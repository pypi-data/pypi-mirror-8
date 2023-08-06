"""
Data models for "studies" studies include attributes about the data and are
heavier in terms of data load
"""
import json
import os
import sys
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import semantic_version

from .metadata import MetaData, PHENOTYPE_COL, POOLED_COL
from .expression import ExpressionData, SpikeInData
from .quality_control import MappingStatsData, MIN_READS
from .splicing import SplicingData, FRACTION_DIFF_THRESH
from ..compute.predict import PredictorConfigManager
from ..datapackage import datapackage_url_to_dict, \
    check_if_already_downloaded, make_study_datapackage
from ..visualize.color import blue
from ..visualize.ipython_interact import Interactive
from ..datapackage import FLOTILLA_DOWNLOAD_DIR
from ..util import load_csv, load_json, load_tsv, load_gzip_pickle_df, \
    load_pickle_df, timestamp, cached_property


SPECIES_DATA_PACKAGE_BASE_URL = 'http://sauron.ucsd.edu/flotilla_projects'
DATAPACKAGE_RESOURCE_COMMON_KWS = ('url', 'path', 'format', 'compression',
                                   'name')


class Study(object):
    """A biological study, with associated metadata, expression, and splicing
    data.
    """
    default_feature_set_ids = []

    # Data types with enough data that we'd probably reduce them, and even
    # then we might want to take subsets. E.g. most variant genes for
    # expression. But we don't expect to do this for spikein or mapping_stats
    # data
    _subsetable_data_types = ['expression', 'splicing']

    initializers = {'metadata_data': MetaData,
                    'expression_data': ExpressionData,
                    'splicing_data': SplicingData,
                    'mapping_stats_data': MappingStatsData,
                    'spikein_data': SpikeInData}

    readers = {'tsv': load_tsv,
               'csv': load_csv,
               'json': load_json,
               'pickle_df': load_pickle_df,
               'gzip_pickle_df': load_gzip_pickle_df}

    _default_reducer_kwargs = {'whiten': False,
                               'show_point_labels': False,
                               'show_vectors': False}

    _default_plot_kwargs = {'marker': 'o', 'color': blue}

    def __init__(self, sample_metadata, version='0.1.0', expression_data=None,
                 expression_feature_data=None,
                 expression_feature_rename_col=None,
                 expression_feature_ignore_subset_cols=None,
                 expression_log_base=None,
                 expression_thresh=-np.inf,
                 expression_plus_one=False,
                 splicing_data=None,
                 splicing_feature_data=None,
                 splicing_feature_rename_col=None,
                 splicing_feature_ignore_subset_cols=None,
                 splicing_feature_expression_id_col=None,
                 mapping_stats_data=None,
                 mapping_stats_number_mapped_col=None,
                 mapping_stats_min_reads=MIN_READS,
                 spikein_data=None,
                 spikein_feature_data=None,
                 drop_outliers=True, species=None,
                 gene_ontology_data=None,
                 predictor_config_manager=None,
                 metadata_pooled_col=POOLED_COL,
                 metadata_phenotype_col=PHENOTYPE_COL,
                 metadata_phenotype_order=None,
                 metadata_phenotype_to_color=None,
                 metadata_phenotype_to_marker=None,
                 license=None, title=None, sources=None,
                 default_sample_subset="all_samples",
                 default_feature_subset="variant",
                 metadata_minimum_samples=0):
        """Construct a biological study

        This class only accepts data, no filenames. All data must already
        have been read in and exist as Python objects.

        Parameters
        ----------
        sample_metadata : pandas.DataFrame
            The only required parameter. Samples as the index, with features as
            columns. Required column: "phenotype". If there is a boolean
            column "pooled", this will be used to separate pooled from single
            cells. Similarly, the column "outliers" will also be used to
            separate outlier cells from the rest.
        version : str
            A string describing the semantic version of the data. Must be in:
            major.minor.patch format, as the "patch" number will be increased
            if you change something in the study and then study.save() it.
            (default "0.1.0")
        expression_data : pandas.DataFrame
            Samples x feature dataframe of gene expression measurements,
            e.g. from an RNA-Seq or a microarray experiment. Assumed to be
            log-transformed, i.e. you took the log of it. (default None)
        expression_feature_data : pandas.DatFrame
            Features x annotations dataframe describing other parameters
            of the gene expression features, e.g. mapping Ensembl IDs to gene
            symbols or gene biotypes. (default None)
        expression_feature_rename_col : str
            A column name in the expression_feature_data dataframe that you'd
            like to rename the expression features to, in the plots. For
            example, if your gene IDs are Ensembl IDs, but you want to plot
            UCSC IDs, make sure the column you want, e.g. "ucsc_id" is in your
            dataframe and specify that. (default "gene_name")
        expression_log_base : float
            If you want to log-transform your expression data (and it's not
            already log-transformed), use this number as the base of the
            transform. E.g. expression_log_base=10 will take the log10 of
            your data. (default None)
        thresh : float
            Minimum (non log-transformed) expression value. (default -inf)
        expression_plus_one : bool
            Whether or not to add 1 to the expression data. (default False)
        splicing_data : pandas.DataFrame
            Samples x feature dataframe of percent spliced in scores, e.g. as
            measured by the program MISO. Assumed that these values only fall
            between 0 and 1.
        splicing_feature_data : pandas.DataFrame
            features x other_features dataframe describing other parameters
            of the splicing features, e.g. mapping MISO IDs to Ensembl IDs or
            gene symbols or transcript types
        splicing_feature_rename_col : str
            A column name in the splicing_feature_data dataframe that you'd
            like to rename the splicing features to, in the plots. For
            example, if your splicing IDs are MISO IDs, but you want to plot
            Ensembl IDs, make sure the column you want, e.g. "ensembl_id" is
            in your dataframe and specify that. Default "gene_name".
        splicing_feature_expression_id_col : str
            A column name in the splicing_feature_data dataframe that
            corresponds to the row names of the expression data
        mapping_stats_data : pandas.DataFrame
            Samples x feature dataframe of mapping stats measurements.
            Currently, this
        mapping_stats_number_mapped_col : str
            A column name in the mapping_stats_data which specifies the
            number of (uniquely or not) mapped reads. Default "Uniquely
            mapped reads number"
        spikein_data : pandas.DataFrame
            samples x features DataFrame of spike-in expression values
        spikein_feature_data : pandas.DataFrame
            Features x other_features dataframe, e.g. of the molecular
            concentration of particular spikein transcripts
        drop_outliers : bool
            Whether or not to drop samples indicated as outliers in the
            sample_metadata from the other data, i.e. with a column
            named 'outlier' in sample_metadata, then remove those
            samples from expression_data for further analysis
        species : str
            Name of the species and genome version, e.g. 'hg19' or 'mm10'.
        gene_ontology_data : pandas.DataFrame
            Gene ids x ontology categories dataframe used for GO analysis.
        metadata_pooled_col : str
            Column in metadata_data which specifies as a boolean
            whether or not this sample was pooled.

        Note
        ----
        This function explicitly specifies ALL the instance variables (except
        those that are marked by the @property decorator), because,
        as described [1], "If you write initialization functions separate from
        __init__ then experienced developers will certainly see your code as a
        kid's playground."

        [1] http://stackoverflow.com/q/12513185/1628971
        """
        sys.stdout.write("{}\tInitializing Study\n".format(timestamp()))
        sys.stdout.write("{}\tInitializing Predictor configuration manager "
                         "for Study\n".format(timestamp()))
        self.predictor_config_manager = predictor_config_manager \
            if predictor_config_manager is not None \
            else PredictorConfigManager()
        # self.predictor_config_manager = None

        self.species = species
        self.gene_ontology_data = gene_ontology_data

        self.license = license
        self.title = title
        self.sources = sources
        self.version = version

        sys.stdout.write('{}\tLoading metadata\n'.format(timestamp()))
        self.metadata = MetaData(
            sample_metadata, metadata_phenotype_order,
            metadata_phenotype_to_color,
            metadata_phenotype_to_marker, pooled_col=metadata_pooled_col,
            phenotype_col=metadata_phenotype_col,
            predictor_config_manager=self.predictor_config_manager)

        self.phenotype_col = self.metadata.phenotype_col
        self.phenotype_order = self.metadata.phenotype_order
        self.phenotype_to_color = self.metadata.phenotype_to_color
        self.phenotype_to_marker = self.metadata.phenotype_to_marker
        self.phenotype_color_ordered = self.metadata.phenotype_color_order
        self.sample_id_to_phenotype = self.metadata.sample_id_to_phenotype
        self.sample_id_to_color = self.metadata.sample_id_to_color
        self.phenotype_transitions = self.metadata.phenotype_transitions

        self.default_feature_subset = default_feature_subset
        self.default_sample_subset = default_sample_subset

        if 'outlier' in self.metadata.data and drop_outliers:
            outliers = self.metadata.data.index[
                self.metadata.data.outlier.astype(bool)]
        else:
            outliers = None
            self.metadata.data['outlier'] = False

        # Get pooled samples
        pooled = None
        if self.metadata.pooled_col is not None:
            if self.metadata.pooled_col in self.metadata.data:
                try:
                    pooled = self.metadata.data.index[
                        self.metadata.data[
                            self.metadata.pooled_col].astype(bool)]
                except:
                    pooled = None
        self.pooled = pooled

        if mapping_stats_data is not None:
            self.mapping_stats = MappingStatsData(
                mapping_stats_data,
                number_mapped_col=mapping_stats_number_mapped_col,
                predictor_config_manager=self.predictor_config_manager,
                min_reads=mapping_stats_min_reads)
            self.technical_outliers = self.mapping_stats.too_few_mapped
            sys.stderr.write('Samples had too few mapped reads (<{'
                             ':.1e} reads):\n\t{}\n'.format(
                mapping_stats_min_reads, ', '.join(self.technical_outliers)))
        else:
            self.technical_outliers = None

        if self.species is not None and (expression_feature_data is None or
                                                 splicing_feature_data is None):
            sys.stdout.write('{}\tLoading species metadata from '
                             '~/flotilla_packages\n'.format(timestamp()))
            species_kws = self.load_species_data(self.species, self.readers)
            expression_feature_data = species_kws.pop('expression_feature_data',
                                                      None)
            expression_feature_rename_col = species_kws.pop(
                'expression_feature_rename_col', None)
            splicing_feature_data = species_kws.pop('splicing_feature_data',
                                                    None)
            splicing_feature_rename_col = species_kws.pop(
                'splicing_feature_rename_col', None)

            if expression_feature_data is None:
                expression_feature_data = species_kws.pop(
                    'expression_feature_data',
                    None)

            if expression_feature_rename_col is None:
                expression_feature_rename_col = species_kws.pop(
                    'expression_feature_rename_col', None)

            if splicing_feature_data is None:
                splicing_feature_data = species_kws.pop(
                    'splicing_feature_data',
                    None)

            if splicing_feature_rename_col is None:
                splicing_feature_rename_col = species_kws.pop(
                    'splicing_feature_rename_col', None)

        if expression_data is not None:
            sys.stdout.write(
                "{}\tLoading expression data\n".format(timestamp()))
            self.expression = ExpressionData(
                expression_data,
                feature_data=expression_feature_data,
                thresh=expression_thresh,
                feature_rename_col=expression_feature_rename_col,
                outliers=outliers, plus_one=expression_plus_one,
                log_base=expression_log_base, pooled=pooled,
                predictor_config_manager=self.predictor_config_manager,
                technical_outliers=self.technical_outliers,
                minimum_samples=metadata_minimum_samples,
                feature_ignore_subset_cols=expression_feature_ignore_subset_cols)
            self.default_feature_set_ids.extend(self.expression.feature_subsets
                                                .keys())
        if splicing_data is not None:
            sys.stdout.write("{}\tLoading splicing data\n".format(
                timestamp()))
            self.splicing = SplicingData(
                splicing_data, feature_data=splicing_feature_data,
                feature_rename_col=splicing_feature_rename_col,
                outliers=outliers, pooled=pooled,
                predictor_config_manager=self.predictor_config_manager,
                technical_outliers=self.technical_outliers,
                minimum_samples=metadata_minimum_samples,
                feature_ignore_subset_cols=splicing_feature_ignore_subset_cols,
                feature_expression_id_col=splicing_feature_expression_id_col)

        if spikein_data is not None:
            self.spikein = SpikeInData(
                spikein_data, feature_data=spikein_feature_data,
                technical_outliers=self.technical_outliers,
                predictor_config_manager=self.predictor_config_manager)
        sys.stdout.write("{}\tSuccessfully initialized a Study "
                         "object!\n".format(timestamp()))

    def __setattr__(self, key, value):
        """Check if the attribute already exists and warns on overwrite.
        """
        if hasattr(self, key):
            warnings.warn('Over-writing attribute {}'.format(key))
        super(Study, self).__setattr__(key, value)

    @property
    def default_sample_subsets(self):
        #move default_sample_subset to the front of the list, sort the rest
        sorted_sample_subsets = list(sorted(list(set(
            self.metadata.sample_subsets.keys()).difference(
            set(self.default_sample_subset)))))
        sorted_sample_subsets.insert(0, self.default_sample_subset)
        return sorted_sample_subsets

    @property
    def default_feature_subsets(self):
        feature_subsets = {}
        for name in self._subsetable_data_types:
            try:
                data_type = getattr(self, name)
            except AttributeError:
                continue
            feature_subsets[name] = data_type.feature_subsets
        return feature_subsets

    @classmethod
    def from_datapackage_url(
            cls, datapackage_url,
            load_species_data=True,
            species_datapackage_base_url=SPECIES_DATA_PACKAGE_BASE_URL):
        """Create a study from a url of a datapackage.json file

        Parameters
        ----------
        datapackage_url : str
            HTTP url of a datapackage.json file, following the specification
            described here: http://dataprotocols.org/data-packages/ and
            requiring the following data resources: metadata,
            expression, splicing
        species_data_pacakge_base_url : str
            Base URL to fetch species-specific gene and splicing event
            metadata from. Default 'http://sauron.ucsd.edu/flotilla_projects'

        Returns
        -------
        study : Study
            A "study" object containing the data described in the
            datapackage_url file

        Raises
        ------
        AttributeError
            If the datapackage.json file does not contain the required
            resources of metadata, expression, and splicing.
        """
        datapackage = datapackage_url_to_dict(datapackage_url)
        datapackage_dir = '{}/{}'.format(FLOTILLA_DOWNLOAD_DIR, 
                                         datapackage['name'])
        return cls.from_datapackage(
            datapackage, load_species_data=load_species_data,
            datapackage_dir=datapackage_dir,
            species_datapackage_base_url=species_datapackage_base_url)

    @classmethod
    def from_datapackage_file(
            cls, datapackage_filename,
            load_species_data=True,
            species_datapackage_base_url=SPECIES_DATA_PACKAGE_BASE_URL):
        with open(datapackage_filename) as f:
            sys.stdout.write('{}\tReading datapackage from {}\n'.format(
                timestamp(), datapackage_filename))
            datapackage = json.load(f)
        datapackage_dir = os.path.dirname(datapackage_filename)
        return cls.from_datapackage(
            datapackage, datapackage_dir=datapackage_dir,
            load_species_data=load_species_data,
            species_datapackage_base_url=species_datapackage_base_url)

    @staticmethod
    def _is_absolute_path(location):
        return location.startswith('http') or location.startswith('/')

    @classmethod
    def from_datapackage(
            cls, datapackage, datapackage_dir='./',
            load_species_data=True,
            species_datapackage_base_url=SPECIES_DATA_PACKAGE_BASE_URL):
        """Create a study object from a datapackage dictionary

        Parameters
        ----------
        datapackage : dict


        Returns
        -------
        study : flotilla.Study
            Study object
        """
        sys.stdout.write('{}\tParsing datapackage to create a Study '
                         'object\n'.format(timestamp()))
        dfs = {}
        kwargs = {}
        datapackage_name = datapackage['name']

        for resource in datapackage['resources']:
            if 'url' in resource:
                resource_url = resource['url']
                if not cls._is_absolute_path(resource_url):
                    resource_url = '{}/{}'.format(datapackage_dir,
                                                  resource_url)
                filename = check_if_already_downloaded(resource_url,
                                                       datapackage_name)
            else:
                if resource['path'].startswith('http'):
                    filename = check_if_already_downloaded(resource['path'],
                                                           datapackage_name)
                else:
                    filename = resource['path']
                    if not cls._is_absolute_path(filename):
                        filename = '{}/{}'.format(datapackage_dir,
                                                  filename)

                    # Test if the file exists, if not, then add the datapackage
                    # file
                    try:
                        with open(filename) as f:
                            pass
                    except IOError:
                        filename = os.path.join(datapackage_dir, filename)

            name = resource['name']

            reader = cls.readers[resource['format']]
            compression = None if 'compression' not in resource else \
                resource['compression']
            header = resource.pop('header', 0)

            dfs[name] = reader(filename, compression=compression,
                               header=header)

            for key in set(resource.keys()).difference(
                    DATAPACKAGE_RESOURCE_COMMON_KWS):
                kwargs['{}_{}'.format(name, key)] = resource[key]

        species_kws = {}
        species = None if 'species' not in datapackage else datapackage[
            'species']
        if load_species_data and species is not None:
            species_kws = cls.load_species_data(species, cls.readers,
                                                species_datapackage_base_url)

        try:
            sample_metadata = dfs.pop('metadata')
        except KeyError:
            raise AttributeError('The datapackage.json file is required to '
                                 'have the "metadata" resource')
        dfs = dict(('{}_data'.format(k), v) for k, v in dfs.iteritems())

        nones = [k for k, v in kwargs.iteritems() if v is None]
        for key in nones:
            kwargs.pop(key)
        kwargs.update(species_kws)
        kwargs.update(dfs)

        license = None if 'license' not in datapackage else datapackage[
            'license']
        title = None if 'title' not in datapackage else datapackage[
            'title']
        sources = None if 'sources' not in datapackage else datapackage[
            'sources']
        version = None if 'datapackage_version' not in datapackage else \
            datapackage['datapackage_version']
        if not semantic_version.validate(version):
            raise ValueError('{} is not a valid version string. Please use '
                             'semantic versioning, with major.minor.patch, '
                             'e.g. 0.1.2 is a valid version string'.format(
                version))
        study = Study(
            sample_metadata=sample_metadata,
            species=species,
            license=license,
            title=title,
            sources=sources,
            version=version,
            **kwargs)
        return study

    @staticmethod
    def load_species_data(species, readers,
                          species_datapackage_base_url=SPECIES_DATA_PACKAGE_BASE_URL):
        dfs = {}

        try:
            species_data_url = '{}/{}/datapackage.json'.format(
                species_datapackage_base_url, species)
            species_datapackage = datapackage_url_to_dict(
                species_data_url)

            for resource in species_datapackage['resources']:
                if 'url' in resource:
                    resource_url = resource['url']
                    filename = check_if_already_downloaded(resource_url,
                                                           species)
                else:
                    filename = resource['path']

                reader = readers[resource['format']]

                compression = None if 'compression' not in resource else \
                    resource['compression']
                name = resource['name']
                dfs[name] = reader(filename,
                                   compression=compression)
                other_keys = set(resource.keys()).difference(
                    DATAPACKAGE_RESOURCE_COMMON_KWS)
                name_no_data = name.rstrip('_data')
                for key in other_keys:
                    new_key = '{}_{}'.format(name_no_data, key)
                    dfs[new_key] = resource[key]
        except (IOError, ValueError) as e:
            sys.stderr.write('Error loading species {} data '.format(species))
            pass
        return dfs

    def detect_outliers(self, data_type='expression',
                        sample_subset=None, feature_subset=None,
                        featurewise=False,
                        reducer=None,
                        standardize=None,
                        reducer_kwargs=None,
                        bins=None,
                        outlier_detection_method=None,
                        outlier_detection_method_kwargs=None):

        if sample_subset is None:
            sample_subset = self.default_sample_subset

        sample_ids = self.sample_subset_to_sample_ids(sample_subset)

        if feature_subset is None:
            feature_subset = self.default_feature_subset

        feature_ids = self.feature_subset_to_feature_ids(data_type,
                                                         feature_subset,
                                                         rename=False)
        if data_type == "expression":
            datamodel = self.expression
        elif data_type == "splicing":
            datamodel = self.splicing

        reducer, outlier_detector = datamodel.detect_outliers(
            sample_ids=sample_ids, feature_ids=feature_ids,
            featurewise=featurewise, reducer=reducer, standardize=standardize,
            reducer_kwargs=reducer_kwargs, bins=bins,
            outlier_detection_method=outlier_detection_method,
            outlier_detection_method_kwargs=outlier_detection_method_kwargs)

        outlier_detector.predict(reducer.reduced_space)
        outlier_detector.title = "_".join(
            ['outlier', data_type, sample_subset, feature_subset])
        print "setting outlier type:\"{}\" in metadata".format(
            outlier_detector.title)
        if outlier_detector.title not in self.metadata.data:
            self.metadata.data[outlier_detector.title] = False

        self.metadata.data[outlier_detector.title].update(
            outlier_detector.outliers)
        return reducer, outlier_detector

    def drop_outliers(self):
        """Assign samples marked as "outlier" in metadata, to other datas"""
        outliers = self.metadata.data['outlier'][
            self.metadata.data['outlier']].index
        self.expression.outlier_samples = outliers
        self.splicing.outlier_samples = outliers

    def jsd(self):
        """Performs Jensen-Shannon Divergence on both splicing and expression
        study_data

        Jensen-Shannon divergence is a method of quantifying the amount of
        change in distribution of one measurement (e.g. a splicing event or a
        gene expression) from one celltype to another.
        """
        raise NotImplementedError
        # TODO: Check if JSD has not already been calculated (memoize)
        self.expression.jsd()
        self.splicing.jsd()

    def normalize_to_spikein(self):
        raise NotImplementedError

    def compute_expression_splicing_covariance(self):
        raise NotImplementedError

    @staticmethod
    def maybe_make_directory(filename):
        # Make the directory if it's not already there
        try:
            directory = os.path.abspath(os.path.dirname(filename))
            os.makedirs(os.path.abspath(directory))
        except OSError:
            pass

    def feature_subset_to_feature_ids(self, data_type, feature_subset=None,
                                      rename=False):
        """Given a name of a feature subset, get the associated feature ids

        Parameters
        ----------
        data_type : str
            A string describing the data type, e.g. "expression"
        feature_subset : str
            A string describing the subset of data type (must be already
            calculated)

        Returns
        -------
        feature_ids : list of strings
            List of features ids from the specified datatype
        """
        if 'expression'.startswith(data_type):
            return self.expression.feature_subset_to_feature_ids(
                feature_subset, rename)
        elif 'splicing'.startswith(data_type):
            return self.splicing.feature_subset_to_feature_ids(
                feature_subset, rename)

    def sample_subset_to_sample_ids(self, phenotype_subset=None):

        """Convert a string naming a subset of phenotypes in the data into
        sample ids

        Parameters
        ----------
        phenotype_subset : str
            A valid string describing a boolean phenotype described in the
            metadata data

        Returns
        -------
        sample_ids : list of strings
            List of sample ids in the data
        """

        # IF this is a list of IDs

        try:
            return self.metadata.sample_subsets[phenotype_subset]
        except KeyError:
            pass

        ind = self.metadata.phenotype_series == phenotype_subset
        if ind.sum() > 0:
            return self.metadata.phenotype_series.index[ind]

        try:
            if phenotype_subset is None or 'all_samples'.startswith(
                    phenotype_subset):
                sample_ind = np.ones(self.metadata.data.shape[0],
                                     dtype=bool)
            elif phenotype_subset.startswith("~"):
                sample_ind = ~pd.Series(
                    self.metadata.data[phenotype_subset.lstrip("~")],
                    dtype='bool')

            else:
                sample_ind = pd.Series(
                    self.metadata.data[phenotype_subset], dtype='bool')
            sample_ids = self.metadata.data.index[sample_ind]
            return sample_ids
        except AttributeError:
            return phenotype_subset

    def plot_pca(self, data_type='expression', x_pc=1, y_pc=2,
                 sample_subset=None, feature_subset=None,
                 title='', featurewise=False, plot_violins=False,
                 show_point_labels=False, reduce_kwargs=None,
                 **kwargs):
        """Performs DataFramePCA on both expression and splicing study_data

        Parameters
        ----------
        data_type : str
            One of the names of the data types, e.g. "expression" or
            "splicing"
        x_pc : int
            Which principal component to plot on the x-axis
        y_pc : int
            Which principal component to plot on the y-axis
        sample_subset : str or None
            Which subset of the samples to use, based on some phenotype
            column in the experiment design data. If None, all samples are
            used.
        feature_subset : str or None
            Which subset of the features to used, based on some feature type
            in the expression data (e.g. "variant"). If None, all features
            are used.
        title : str
            The title of the plot
        plot_violins : bool
            Whether or not to make the violinplots of the top features. This
            can take a long time, so to save time you can turn it off if you
            just want a quick look at the PCA.
        show_point_labels : bool
            Whether or not to show the labels of the points. If this is
            samplewise (default), then this labels the samples. If this is
            featurewise, then this labels the features.
        """

        sample_subset = self.default_sample_subset if sample_subset is None else sample_subset
        feature_subset = self.default_feature_subset if feature_subset is None else feature_subset

        sample_ids = self.sample_subset_to_sample_ids(sample_subset)
        feature_ids = self.feature_subset_to_feature_ids(data_type,
                                                         feature_subset,
                                                         rename=False)

        if not featurewise:
            label_to_color = self.phenotype_to_color
            label_to_marker = self.phenotype_to_marker
            groupby = self.sample_id_to_phenotype
            order = self.phenotype_order
        else:
            label_to_color = None
            label_to_marker = None
            groupby = None
            order = None

        if "expression".startswith(data_type):
            reducer = self.expression.plot_pca(
                x_pc=x_pc, y_pc=y_pc, sample_ids=sample_ids,
                feature_ids=feature_ids,
                label_to_color=label_to_color,
                label_to_marker=label_to_marker, groupby=groupby,
                order=order,
                featurewise=featurewise, show_point_labels=show_point_labels,
                title=title, reduce_kwargs=reduce_kwargs,
                plot_violins=plot_violins, **kwargs)

        elif "splicing".startswith(data_type):
            reducer = self.splicing.plot_pca(
                x_pc=x_pc, y_pc=y_pc, sample_ids=sample_ids,
                feature_ids=feature_ids,
                label_to_color=label_to_color,
                label_to_marker=label_to_marker, groupby=groupby,
                order=order,
                featurewise=featurewise, show_point_labels=show_point_labels,
                title=title, reduce_kwargs=reduce_kwargs,
                plot_violins=plot_violins, **kwargs)
        else:
            raise ValueError('The data type {} does not exist in this study'
                             .format(data_type))
        return reducer

    def plot_graph(self, data_type='expression', sample_subset=None,
                   feature_subset=None, featurewise=False,
                   **kwargs):
        """Plot the graph (network) of these data

        Parameters
        ----------
        data_type : str
            One of the names of the data types, e.g. "expression" or "splicing"
        sample_subset : str or None
            Which subset of the samples to use, based on some phenotype
            column in the experiment design data. If None, all samples are
            used.
        feature_subset : str or None
            Which subset of the features to used, based on some feature type
            in the expression data (e.g. "variant"). If None, all features
            are used.
        """
        sample_ids = self.sample_subset_to_sample_ids(sample_subset)
        feature_ids = self.feature_subset_to_feature_ids(data_type,
                                                         feature_subset,
                                                         rename=False)

        if not featurewise:
            label_to_color = self.phenotype_to_color
            label_to_marker = self.phenotype_to_marker
            groupby = self.sample_id_to_phenotype
        else:
            label_to_color = None
            label_to_marker = None
            groupby = None

        if data_type == "expression":
            return self.expression.networks.draw_graph(
                sample_ids=sample_ids, feature_ids=feature_ids,
                sample_id_to_color=self.sample_id_to_color,
                label_to_color=label_to_color,
                label_to_marker=label_to_marker, groupby=groupby,
                featurewise=featurewise,
                **kwargs)
        elif data_type == "splicing":
            return self.splicing.networks.draw_graph(
                sample_ids=sample_ids, feature_ids=feature_ids,
                sample_id_to_color=self.sample_id_to_color,
                label_to_color=label_to_color,
                label_to_marker=label_to_marker, groupby=groupby,
                featurewise=featurewise,
                **kwargs)

    def plot_study_sample_legend(self):
        markers = self.metadata.data.color.groupby(
            self.metadata.data.marker
            + "." + self.metadata.data.celltype).last()

        f, ax = plt.subplots(1, 1, figsize=(3, len(markers)))

        for i, point_type in enumerate(markers.iteritems(), ):
            mrk, celltype = point_type[0].split('.')
            ax.scatter(0, 0, marker=mrk, c=point_type[1],
                       edgecolor='none', label=celltype,
                       s=160)
        ax.set_xlim(1, 2)
        ax.set_ylim(1, 2)
        ax.axis('off')
        legend = ax.legend(title='cell type', fontsize=20, )
        return legend

    def plot_classifier(self, trait, sample_subset=None,
                        feature_subset='all_genes',
                        data_type='expression', title='',
                        show_point_labels=False,
                        **kwargs):
        """Plot a predictor for the specified data type and trait(s)

        Parameters
        ----------
        data_type : str
            One of the names of the data types, e.g. "expression" or "splicing"
        trait : str
            Column name in the metadata data that you would like
            to classify on

        Returns
        -------


        """
        try:
            trait_data = self.metadata.data[trait]
        except KeyError:
            trait_ids = self.metadata.sample_subsets[trait]
            trait_data = self.metadata.data.index.isin(trait_ids)
        if all(trait_data == True) or all(trait_data == False) or len(
                set(trait_data)) <= 1:
            raise ValueError("All samples are True (or all samples are "
                             "False) or all are the same, cannot classify"
                             "when all samples are the same")
        trait_data = pd.Series(trait_data, name=trait,
                               index=self.metadata.data.index)

        sample_ids = self.sample_subset_to_sample_ids(sample_subset)
        feature_ids = self.feature_subset_to_feature_ids(data_type,
                                                         feature_subset,
                                                         rename=False)
        feature_subset = 'none' if feature_subset is None else feature_subset
        sample_subset = 'none' if sample_subset is None else sample_subset
        data_name = '_'.join([sample_subset, feature_subset])

        label_to_color = self.phenotype_to_color
        label_to_marker = self.phenotype_to_marker
        groupby = self.sample_id_to_phenotype

        order = self.phenotype_order
        color = self.phenotype_color_ordered

        if data_type == "expression":
            self.expression.plot_classifier(
                data_name=data_name, trait=trait_data,
                sample_ids=sample_ids, feature_ids=feature_ids,
                label_to_color=label_to_color,
                label_to_marker=label_to_marker, groupby=groupby,
                show_point_labels=show_point_labels, title=title,
                order=order, color=color,
                **kwargs)
        elif data_type == "splicing":
            self.splicing.plot_classifier(
                data_name=data_name, trait=trait_data,
                sample_ids=sample_ids, feature_ids=feature_ids,
                label_to_color=label_to_color,
                label_to_marker=label_to_marker, groupby=groupby,
                show_point_labels=show_point_labels, title=title,
                order=order, color=color,
                **kwargs)

    def plot_regressor(self, data_type='expression', **kwargs):
        """
        """
        raise NotImplementedError
        if data_type == "expression":
            self.expression.plot_regressor(**kwargs)
        elif data_type == "splicing":
            self.splicing.plot_regressor(**kwargs)

    def modalities(self, sample_subset=None, feature_subset=None,
                   expression_thresh=-np.inf, bootstrapped=False,
                   bootstrapped_kws=None):
        """Get splicing modality assignments of data

        Parameters
        ----------
        sample_subset : str or None, optional
            Which subset of the samples to use, based on some phenotype
            column in the experiment design data. If None, all samples are
            used.
        feature_subset : str or None, optional
            Which subset of the features to used, based on some feature type
            in the expression data (e.g. "variant"). If None, all features
            are used.
        expression_thresh : float, optional
            Minimum expression value, of the original input. E.g. if the
            original input is already log-transformed, then this threshold is
            on the log values.
        bootstrapped : bool, optional
            Whether or not to use bootstrap resampling of each splicing event
            to robustly estimate its modality
        bootstrapped_kws : dict, optional
            Valid arguments to _bootstrapped_fit_transform. If None, default is
            dict(n_iter=100, thresh=0.6, minimum_samples=10)

        Returns
        -------
        modalities : pandas.Series
            A (n_events,) shaped series of the assigned modality (in the case
            of bootstrapped=False), or modality most commonly assigned, in the
            case of bootstrapped=True

        """
        if expression_thresh > -np.inf:
            data = self.filter_splicing_on_expression(
                expression_thresh=expression_thresh,
                sample_subset=sample_subset)
            sample_ids = None
            feature_ids = None
        else:
            sample_ids = self.sample_subset_to_sample_ids(sample_subset)
            feature_ids = self.feature_subset_to_feature_ids(
                'splicing', feature_subset, rename=False)
            data = None

        return self.splicing.modalities(sample_ids, feature_ids, data=data,
                                        bootstrapped=bootstrapped,
                                        groupby=self.sample_id_to_phenotype,
                                        bootstrapped_kws=bootstrapped_kws)

    def modalities_counts(self, sample_subset=None, feature_subset=None,
                   expression_thresh=-np.inf, bootstrapped=True,
                   bootstrapped_kws=None):
        """Get counts of each resampled splicing event assigned to a modality

        Parameters
        ----------
        sample_subset : str or None, optional
            Which subset of the samples to use, based on some phenotype
            column in the experiment design data. If None, all samples are
            used.
        feature_subset : str or None, optional
            Which subset of the features to used, based on some feature type
            in the expression data (e.g. "variant"). If None, all features
            are used.
        expression_thresh : float, optional
            Minimum expression value, of the original input. E.g. if the
            original input is already log-transformed, then this threshold is
            on the log values.
        bootstrapped : bool, optional
            Whether or not to use bootstrap resampling of each splicing event
            to robustly estimate its modality
        bootstrapped_kws : dict, optional
            Valid arguments to _bootstrapped_fit_transform. If None, default is
            dict(n_iter=100, thresh=0.6, minimum_samples=10)

        Returns
        -------
        modalities : pandas.Series
            A (n_events,) shaped series of the assigned modality (in the case
            of bootstrapped=False), or modality most commonly assigned, in the
            case of bootstrapped=True

        """
        if expression_thresh > -np.inf:
            data = self.filter_splicing_on_expression(
                expression_thresh=expression_thresh,
                sample_subset=sample_subset)
            sample_ids = None
            feature_ids = None
        else:
            sample_ids = self.sample_subset_to_sample_ids(sample_subset)
            feature_ids = self.feature_subset_to_feature_ids(
                'splicing', feature_subset, rename=False)
            data = None

        return self.splicing.modalities_counts(
            sample_ids, feature_ids, data=data, bootstrapped=bootstrapped,
            bootstrapped_kws=bootstrapped_kws,
            groupby=self.sample_id_to_phenotype)

    def plot_modalities(self, sample_subset=None, feature_subset=None,
                        normed=True, bootstrapped=False,
                        bootstrapped_kws=None, expression_thresh=-np.inf):
        # try:
        if expression_thresh > -np.inf:
            data = self.filter_splicing_on_expression(
                expression_thresh=expression_thresh,
                sample_subset=sample_subset)
            sample_ids = None
            feature_ids = None
        else:
            sample_ids = self.sample_subset_to_sample_ids(sample_subset)
            feature_ids = self.feature_subset_to_feature_ids(
                'splicing', feature_subset, rename=False)
            data = None

        grouped = self.sample_id_to_phenotype.groupby(
            self.sample_id_to_phenotype)

        # Account for bar plot and plot of the reduced space of ALL samples
        n = grouped.ngroups + 2
        groups = ['all']
        fig, axes = plt.subplots(ncols=n, figsize=(n * 4, 4))
        bar_ax = axes[0]
        all_ax = axes[1]
        self.splicing.plot_modalities_reduced(sample_ids, feature_ids,
                                              all_ax, title='all samples',
                                              bootstrapped=bootstrapped,
                                              bootstrapped_kws=bootstrapped_kws)
        self.splicing.plot_modalities_stacked_bar(sample_ids, feature_ids,
                                          bar_ax, i=0, normed=normed,
                                          legend=False,
                                          bootstrapped=bootstrapped,
                                          bootstrapped_kws=bootstrapped_kws)

        axes = axes[2:]
        for i, ((celltype, series), ax) in enumerate(zip(grouped, axes)):
            groups.append(celltype)
            sys.stdout.write('\n---- {} ----\n'.format(celltype))
            samples = series.index.intersection(sample_ids)
            # legend = i == 0
            self.splicing.plot_modalities_stacked_bar(samples, feature_ids,
                                              bar_ax, i + 1, normed=normed,
                                              legend=False)

            self.splicing.plot_modalities_reduced(samples, feature_ids,
                                                  ax, title=celltype)

        bar_ax.set_xticks(np.arange(len(groups)) + 0.4)
        bar_ax.set_xticklabels(groups)
        # except AttributeError:
        # pass

    def celltype_sizes(self, data_type='splicing'):
        if data_type == 'expression':
            self.expression.data.groupby(self.sample_id_to_phenotype,
                                         axis=0).size()
        if data_type == 'splicing':
            self.splicing.data.groupby(self.sample_id_to_phenotype,
                                       axis=0).size()

    @property
    def celltype_event_counts(self):
        """Number of cells that detected this event in that celltype
        """
        return self.splicing.data.groupby(
            self.sample_id_to_phenotype, axis=0).apply(
            lambda x: x.groupby(level=0, axis=0).transform(
                lambda x: x.count()).sum()).replace(0, np.nan)

    def unique_celltype_event_counts(self, n=1):
        celltype_event_counts = self.celltype_event_counts
        return celltype_event_counts[celltype_event_counts <= n]

    def percent_unique_celltype_events(self, n=1):
        n_unique = self.unique_celltype_event_counts(n).sum(axis=1)
        n_total = self.celltype_event_counts.sum(axis=1).astype(float)
        return n_unique / n_total * 100

    # @property
    # def celltype_modalities(self):
    #     """Return modality assignments of each celltype
    #     """
    #     return self.splicing.data.groupby(
    #         self.sample_id_to_phenotype, axis=0).apply(
    #         lambda x: self.splicing.modalities(x.index))

    def plot_modalities_lavalamps(self, sample_subset=None, bootstrapped=False,
                                  bootstrapped_kws=None,
                                  expression_thresh=-np.inf):
        # grouped = self.splicing.singles.groupby(self.sample_id_to_phenotype,
        #                                         axis=0)
        # celltype_groups = self.splicing.singles.groupby(
        #     self.sample_id_to_phenotype, axis=0)
        #
        # if sample_subset is not None:
        #     # Only plotting one sample_subset, use the modality assignments
        #     # from just the samples from this sample_subset
        #     celltype_samples = set(celltype_groups.groups[sample_subset])
        # else:
        #     # Plotting all the celltypes, use the modality assignments from
        #     # all celltypes together
        #     celltype_samples = self.splicing.data.index

        if expression_thresh > -np.inf:
            data = self.filter_splicing_on_expression(
                expression_thresh=expression_thresh,
                sample_subset=sample_subset)
            sample_ids = None
        else:
            sample_ids = self.sample_subset_to_sample_ids(sample_subset)
            data = None

        # for i, (phenotype, sample_ids) in enumerate(grouped.groups.iteritems()):
        #     x_offset = 1. / (i + 1)
        #     sample_ids = celltype_samples.intersection(sample_ids)
        #     color = self.phenotype_to_color[phenotype]
        #     if len(sample_ids) > 0:
        self.splicing.plot_modalities_lavalamps(
            groupby=self.sample_id_to_phenotype,
            phenotype_to_color=self.phenotype_to_color,
            sample_ids=sample_ids, data=data,
            # color=color,
            # x_offset=x_offset,
            # title=phenotype,
            bootstrapped=bootstrapped,
            bootstrapped_kws=bootstrapped_kws)

    def plot_event(self, feature_id, sample_subset=None, nmf_space=False):
        """Plot the violinplot and NMF transitions of a splicing event
        """
        sample_ids = self.sample_subset_to_sample_ids(sample_subset)
        self.splicing.plot_feature(feature_id, sample_ids,
                                   phenotype_groupby=self.sample_id_to_phenotype,
                                   phenotype_order=self.phenotype_order,
                                   color=self.phenotype_color_ordered,
                                   phenotype_to_color=self.phenotype_to_color,
                                   phenotype_to_marker=self.phenotype_to_marker,
                                   nmf_space=nmf_space)

    def plot_gene(self, feature_id, sample_subset=None, nmf_space=False):
        sample_ids = self.sample_subset_to_sample_ids(sample_subset)
        self.expression.plot_feature(
            feature_id, sample_ids,
            phenotype_groupby=self.sample_id_to_phenotype,
            phenotype_order=self.phenotype_order,
            color=self.phenotype_color_ordered,
            phenotype_to_color=self.phenotype_to_color,
            phenotype_to_marker=self.phenotype_to_marker, nmf_space=nmf_space)

    def plot_lavalamp_pooled_inconsistent(
            self, sample_subset=None, feature_subset=None,
            fraction_diff_thresh=FRACTION_DIFF_THRESH,
            expression_thresh=-np.inf):
        # grouped_ids = self.splicing.data.groupby(self.sample_id_to_color,
        # axis=0)
        celltype_groups = self.metadata.data.groupby(
            self.sample_id_to_phenotype, axis=0)

        if sample_subset is not None:
            # Only plotting one sample_subset
            celltype_samples = set(celltype_groups.groups[sample_subset])
        else:
            # Plotting all the celltypes
            celltype_samples = self.sample_subset_to_sample_ids(sample_subset)

        feature_ids = self.feature_subset_to_feature_ids('splicing',
                                                            feature_subset=feature_subset)

        celltype_and_sample_ids = celltype_groups.groups.iteritems()
        for i, (phenotype, sample_ids) in enumerate(celltype_and_sample_ids):
            # import pdb; pdb.set_trace()

            # Assumes all samples of a sample_subset have the same color...
            # probably wrong
            color = self.phenotype_to_color[phenotype]
            sample_ids = celltype_samples.intersection(sample_ids)
            if len(sample_ids) == 0:
                continue
            data = self.filter_splicing_on_expression(expression_thresh)
            data = data.ix[sample_ids, :]
            self.splicing.plot_lavalamp_pooled_inconsistent(data,
                feature_ids, fraction_diff_thresh, color=color)

    def percent_pooled_inconsistent(
            self, sample_subset=None, feature_subset=None,
            fraction_diff_thresh=FRACTION_DIFF_THRESH,
            expression_thresh=-np.inf):
        celltype_groups = self.metadata.data.groupby(
            self.sample_id_to_phenotype, axis=0)

        if sample_subset is not None:
            # Only plotting one sample_subset
            celltype_samples = set(celltype_groups.groups[sample_subset])
        else:
            # Plotting all the celltypes
            celltype_samples = self.sample_subset_to_sample_ids(sample_subset)

        feature_ids = self.feature_subset_to_feature_ids('splicing',
                                                         feature_subset=feature_subset)

        celltype_and_sample_ids = celltype_groups.groups.iteritems()
        percents = pd.Series(celltype_groups.groups.keys())
        for i, (phenotype, sample_ids) in enumerate(celltype_and_sample_ids):
            # import pdb; pdb.set_trace()

            # Assumes all samples of a sample_subset have the same color...
            # probably wrong
            color = self.phenotype_to_color[phenotype]
            sample_ids = celltype_samples.intersection(sample_ids)
            if len(sample_ids) == 0:
                continue
            data = self.filter_splicing_on_expression(expression_thresh)
            data = data.ix[sample_ids, :]
            singles, pooled, not_measured_in_pooled, pooled_inconsistent =\
                self.splicing.pooled_inconsistent(data, feature_ids,
                                              fraction_diff_thresh)
            percent = self._percent_pooled_inconsistent(pooled,
                                                        pooled_inconsistent)
            percents[phenotype] = percent
        return percents


    def plot_clustermap(self, sample_subset=None, feature_subset=None,
                        data_type='expression', metric='euclidean',
                        method='average', figsize=None,
                        scale_fig_by_data=True, **kwargs):
        """Visualize hierarchical relationships within samples and features

        Parameters
        ----------


        Returns
        -------


        Raises
        ------
        """

        if feature_subset is None:
            feature_subset = self.default_feature_subset

        sample_ids = self.sample_subset_to_sample_ids(sample_subset)
        feature_ids = self.feature_subset_to_feature_ids(data_type,
                                                         feature_subset,
                                                         rename=False)

        if data_type == "expression":
            return self.expression.plot_clustermap(
                sample_ids=sample_ids, feature_ids=feature_ids, method=method,
                metric=metric, sample_id_to_color=self.sample_id_to_color,
                figsize=figsize, scale_fig_by_data=scale_fig_by_data,
                **kwargs)
        elif data_type == "splicing":
            return self.splicing.plot_clustermap(
                sample_ids=sample_ids, feature_ids=feature_ids, method=method,
                metric=metric, sample_id_to_color=self.sample_id_to_color,
                figsize=figsize, scale_fig_by_data=scale_fig_by_data,
                **kwargs)

    def plot_correlations(self, sample_subset=None, feature_subset=None,
                        data_type='expression', metric='euclidean',
                        method='average', figsize=None, featurewise=False,
                        scale_fig_by_data=True, **kwargs):
        """Visualize clustered correlations of samples across features

        Parameters
        ----------


        Returns
        -------


        Raises
        ------

        """

        if feature_subset is None:
            feature_subset = self.default_feature_subset

        sample_ids = self.sample_subset_to_sample_ids(sample_subset)
        feature_ids = self.feature_subset_to_feature_ids(data_type,
                                                         feature_subset,
                                                         rename=False)

        if figsize is not None and scale_fig_by_data:
            raise ValueError('If "scale_fig_by_data" is true, then cannot '
                             'also specify "figsize"')

        if data_type == "expression":
            return self.expression.plot_correlations(
                sample_ids=sample_ids, feature_ids=feature_ids,
                sample_id_to_color=self.sample_id_to_color,
                figsize=figsize, scale_fig_by_data=scale_fig_by_data,
                metric=metric, method=method, featurewise=featurewise,
                **kwargs)
        elif data_type == "splicing":
            return self.splicing.plot_correlations(
                sample_ids=sample_ids, feature_ids=feature_ids, method=method,
                metric=metric, sample_id_to_color=self.sample_id_to_color,
                figsize=figsize, scale_fig_by_data=scale_fig_by_data,
                featurewise=featurewise, **kwargs)

    def plot_lavalamps(self, sample_subset=None, feature_subset=None,
                       expression_thresh=-np.inf):
        if expression_thresh > -np.inf:
            data = self.filter_splicing_on_expression(
                expression_thresh=expression_thresh,
                sample_subset=sample_subset)
            sample_ids = None
            feature_ids = None
        else:
            sample_ids = self.sample_subset_to_sample_ids(sample_subset)
            feature_ids = self.feature_subset_to_feature_ids(
                'splicing', feature_subset, rename=False)
            data = None

        self.splicing.plot_lavalamp(sample_ids, feature_ids, data,
                                    self.sample_id_to_phenotype,
                                    self.phenotype_to_color,
                                    order=self.phenotype_order)

    def plot_big_nmf_space_transitions(self, data_type='expression', n=5):
        if data_type == 'expression':
            self.expression.plot_big_nmf_space_transitions(
                self.sample_id_to_phenotype, self.phenotype_transitions,
                self.phenotype_order, self.phenotype_color_ordered,
                self.phenotype_to_color, self.phenotype_to_marker, n=n)
        if data_type == 'splicing':
            self.splicing.plot_big_nmf_space_transitions(
                self.sample_id_to_phenotype, self.phenotype_transitions,
                self.phenotype_order, self.phenotype_color_ordered,
                self.phenotype_to_color, self.phenotype_to_marker, n=n)


    def plot_two_samples(self, sample1, sample2, data_type='expression',
                         **kwargs):
        """Plot a scatterplot of two samples' data

        Parameters
        ----------
        sample1 : str
            Name of the sample to plot on the x-axis
        sample2 : str
            Name of the sample to plot on the y-axis
        data_type : "expression" | "splicing"
            Type of data to plot. Default "expression"
        Any other keyword arguments valid for seaborn.jointplot

        Returns
        -------
        jointgrid : seaborn.axisgrid.JointGrid
            Returns a JointGrid instance

        See Also
        -------
        seaborn.jointplot

        """
        if data_type == 'expression':
            return self.expression.plot_two_samples(sample1, sample2, **kwargs)
        elif data_type == 'splicing':
            return self.splicing.plot_two_samples(sample1, sample2, **kwargs)

    def plot_two_features(self, feature1, feature2, data_type='expression',
                          **kwargs):
        """Make a scatterplot of two features' data

        Parameters
        ----------
        feature1 : str
            Name of the feature to plot on the x-axis. If you have a
            feature_data dataframe for this data type, will attempt to map
            the common name, e.g. "RBFOX2" back to the crazy name,
            e.g. "ENSG00000100320"
        feature2 : str
            Name of the feature to plot on the y-axis. If you have a
            feature_data dataframe for this data type, will attempt to map
            the common name, e.g. "RBFOX2" back to the crazy name,
            e.g. "ENSG00000100320"

        Returns
        -------


        Raises
        ------
        """
        if data_type == 'expression':
            self.expression.plot_two_features(
                feature1, feature2, groupby=self.sample_id_to_phenotype,
                label_to_color=self.phenotype_to_color, **kwargs)
        if data_type == 'splicing':
            self.splicing.plot_two_features(
                feature1, feature2, groupby=self.sample_id_to_phenotype,
                label_to_color=self.phenotype_to_color, **kwargs)

    def nmf_space_positions(self, data_type='splicing'):
        if data_type == 'splicing':
            return self.splicing.nmf_space_positions(
                self.sample_id_to_phenotype)

    def nmf_space_transitions(self, phenotype_transitions='all',
                              data_type='splicing', n=5):
        """The change in NMF space of splicing events across phenotypes

        Parameters
        ----------
        phenotype_transitions : list of length-2 tuples of str
            List of ('phenotype1', 'phenotype2') transitions whose change in
            distribution you are interested in
        data_type : 'splicing' | 'expression'
            Which data type to calculate this on. (default='splicing')
        n : int
            Minimum number of samples per phenotype, per event

        Returns
        -------
        big_transitions : pandas.DataFrame
            A (n_events, n_transitions) dataframe of the NMF distances between
            splicing events
        """
        if phenotype_transitions == 'all':
            phenotype_transitions = self.phenotype_transitions
        if data_type == 'splicing':
            return self.splicing.nmf_space_transitions(
                self.sample_id_to_phenotype, phenotype_transitions, n=n)

    def big_nmf_space_transitions(self, phenotype_transitions='all',
                                  data_type='splicing', n=5):
        """Splicing events whose change in NMF space is large

        By large, we mean that difference is 2 standard deviations away from
        the mean

        Parameters
        ----------
        phenotype_transitions : list of length-2 tuples of str
            List of ('phenotype1', 'phenotype2') transitions whose change in
            distribution you are interested in
        data_type : 'splicing' | 'expression'
            Which data type to calculate this on. (default='splicing')
        n : int
            Minimum number of samples per phenotype, per event

        Returns
        -------
        big_transitions : pandas.DataFrame
            A (n_events, n_transitions) dataframe of the NMF distances between
            splicing events
        """
        if phenotype_transitions == 'all':
            phenotype_transitions = self.phenotype_transitions
        if data_type == 'splicing':
            return self.splicing.big_nmf_space_transitions(
                self.sample_id_to_phenotype, phenotype_transitions, n=n)

    def save(self, name, flotilla_dir=FLOTILLA_DOWNLOAD_DIR):

        metadata = self.metadata.data

        metadata_kws = {'pooled_col': self.metadata.pooled_col,
                        'phenotype_col': self.metadata.phenotype_col,
                        'phenotype_order': self.metadata.phenotype_order,
                        'phenotype_to_color':
                            self.metadata.phenotype_to_color,
                        'phenotype_to_marker':
                            self.metadata.phenotype_to_marker,
                        'minimum_samples': self.metadata.minimum_samples}

        try:
            expression = self.expression.data_original
            expression_kws = {
                'log_base': self.expression.log_base,
                'thresh': self.expression.thresh,
                'plus_one': self.expression.plus_one}
        except AttributeError:
            expression = None
            expression_kws = None

        try:
            expression_feature_data = self.expression.feature_data
            expression_feature_kws = {'rename_col':
                                          self.expression.feature_rename_col,
                                      'ignore_subset_cols':
                                          self.expression.feature_ignore_subset_cols}
        except AttributeError:
            expression_feature_data = None
            expression_feature_kws = None

        try:
            splicing = self.splicing.data_original
            splicing_kws = {}
        except AttributeError:
            splicing = None
            splicing_kws = None

        try:
            splicing_feature_data = self.splicing.feature_data
            splicing_feature_kws = {'rename_col':
                                        self.splicing.feature_rename_col,
                                    'ignore_subset_cols':
                                        self.splicing.feature_ignore_subset_cols,
                                    'expression_id_col':
                                        self.splicing.feature_expression_id_col}
        except AttributeError:
            splicing_feature_data = None
            splicing_feature_kws = None

        try:
            spikein = self.spikein.data_original
        except AttributeError:
            spikein = None

        try:
            mapping_stats = self.mapping_stats.data_original
            mapping_stats_kws = {'number_mapped_col':
                                     self.mapping_stats.number_mapped_col}
        except AttributeError:
            mapping_stats = None
            mapping_stats_kws = None


        # Increase the version number
        version = semantic_version.Version(self.version)
        version.patch = version.patch + 1
        version = str(version)

        return make_study_datapackage(name, metadata, expression, splicing,
                                      spikein, mapping_stats,
                                      metadata_kws=metadata_kws,
                                      expression_kws=expression_kws,
                                      splicing_kws=splicing_kws,
                                      mapping_stats_kws=mapping_stats_kws,
                                      expression_feature_kws=expression_feature_kws,
                                      expression_feature_data=expression_feature_data,
                                      splicing_feature_data=splicing_feature_data,
                                      splicing_feature_kws=splicing_feature_kws,
                                      species=self.species,
                                      license=self.license,
                                      title=self.title,
                                      sources=self.sources,
                                      version=version,
                                      flotilla_dir=flotilla_dir)

    @cached_property()
    def tidy_splicing_with_expression(self):
        """A tall 'tidy' dataframe of samples with expression and splicing

        :return:
        :rtype:
        """
        # Tidify splicing
        splicing = self.splicing.data
        splicing_index_name = splicing.index.name
        splicing_index_name = 'index' if splicing_index_name is None \
            else splicing_index_name
        if isinstance(splicing.columns, pd.MultiIndex):
            splicing_columns_name = splicing.columns.names
        else:
            splicing_columns_name = splicing.columns.name

        splicing_tidy = pd.melt(splicing.reset_index(),
                                id_vars=splicing_index_name,
                                value_name='psi',
                                var_name=splicing_columns_name)
        splicing_tidy = splicing_tidy.rename(columns={
            splicing_index_name: 'sample_id'})
        splicing_tidy['common_id'] = splicing_tidy[splicing_columns_name].map(
            self.splicing.feature_data[self.splicing.feature_expression_id_col])

        splicing_tidy = splicing_tidy.dropna()

        # Tidify expression
        expression = self.expression.data_original
        expression_index_name = expression.index.name
        expression_index_name = 'index' if expression_index_name is None \
            else expression_index_name

        expression_tidy = pd.melt(expression.reset_index(),
                                  id_vars=expression_index_name,
                                  value_name='expression',
                                  var_name='common_id')
        # if expression_index_name == 'index':
        expression_tidy = expression_tidy.rename(columns={'index': 'sample_id'})
        expression_tidy = expression_tidy.dropna()

        splicing_tidy.set_index(['sample_id', 'common_id'], inplace=True)
        expression_tidy.set_index(['sample_id', 'common_id'], inplace=True)

        return splicing_tidy.join(expression_tidy, how='inner').reset_index()

    def filter_splicing_on_expression(self, expression_thresh,
                                      sample_subset=None):
        """Filter splicing events on expression values

        Parameters
        ----------
        expression_thresh : float
            Minimum expression value, of the original input. E.g. if the
            original input is already log-transformed, then this threshold is
            on the log values.

        Returns
        -------
        psi : pandas.DataFrame
            A (n_samples, n_features)

        """
        sample_ids = self.sample_subset_to_sample_ids(sample_subset)
        splicing_with_expression = \
            self.tidy_splicing_with_expression.ix[
                self.tidy_splicing_with_expression.sample_id.isin(sample_ids)]
        ind = splicing_with_expression.expression >= expression_thresh
        splicing_high_expression = splicing_with_expression.ix[ind]
        splicing_high_expression = splicing_high_expression.reset_index().dropna()
        filtered_psi = splicing_high_expression.pivot(
            columns='miso_id', index='sample_id', values='psi')
        return filtered_psi



# Add interactive visualizations
Study.interactive_classifier = Interactive.interactive_classifier
Study.interactive_graph = Interactive.interactive_graph
Study.interactive_pca = Interactive.interactive_pca
# Study.interactive_localZ = Interactive.interactive_localZ
Study.interactive_lavalamp_pooled_inconsistent = \
    Interactive.interactive_lavalamp_pooled_inconsistent
Study.interactive_choose_outliers = Interactive.interactive_choose_outliers
Study.interactive_reset_outliers = Interactive.interactive_reset_outliers
Study.interactive_clustermap = Interactive.interactive_clustermap
Study.interactive_correlations = Interactive.interactive_correlations
