import sys

import networkx as nx
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn

from .color import green
from ..compute.network import Networker
from ..util import dict_to_str
from ..visualize.color import blue


class NetworkerViz(Networker):
    # TODO.md: needs to be decontaminated, as it requires methods from
    # data_object;
    # maybe this class should move to data_model.BaseData
    def __init__(self, DataModel):
        self.DataModel = DataModel
        Networker.__init__(self)

    def draw_graph(self,
                   n_pcs=5,
                   use_pc_1=True, use_pc_2=True, use_pc_3=True, use_pc_4=True,
                   degree_cut=2, cov_std_cut=1.8,
                   weight_function='no_weight',
                   featurewise=False,  # else feature_components
                   rpkms_not_events=False,  # else event features
                   feature_of_interest='RBFOX2', draw_labels=True,
                   reduction_name=None,
                   feature_ids=None,
                   sample_ids=None,
                   graph_file='',
                   compare="",
                   sample_id_to_color=None,
                   label_to_color=None,
                   label_to_marker=None, groupby=None,
                   data_type=None):

        """Draw the graph (network) of these events

        Parameters
        ----------
        feature_ids : list of str, or None
            Feature ids to subset the data. If None, all features will be used.
        sample_ids : list of str, or None
            Sample ids to subset the data. If None, all features will be used.
        x_pc : str
            x component for DataFramePCA, default "pc_1"
        y_pc :
            y component for DataFramePCA, default "pc_2"
        n_pcs : int???
            n components to use for cells' covariance calculation
        cov_std_cut : float??
            covariance cutoff for edges
        use_pc{1-4} use these pcs in cov calculation (default True)
        degree_cut : int??
            miniumum degree for a node to be included in graph display
        weight_function : ['arctan' | 'sq' | 'abs' | 'arctan_sq']
            weight function (arctan (arctan cov), sq (sq cov), abs (abs cov),
            arctan_sq (sqared arctan of cov))
        gene_of_interest : str
            map a gradient representing this gene's data onto nodes (ENSEMBL
            id or gene name???)


        Returns
        -------
        #TODO: Mike please fill these in
        graph : ???
            ???
        pos : ???
            ???
        """
        node_color_mapper = self._default_node_color_mapper
        node_size_mapper = self._default_node_color_mapper
        settings = locals().copy()
        # not pertinent to the graph, these are what we want to be able to
        # re-apply to the same graph if it exists
        pca_settings = dict()
        pca_settings['sample_ids'] = sample_ids
        pca_settings['featurewise'] = featurewise
        pca_settings['feature_ids'] = feature_ids
        # pca_settings['obj_id'] = reduction_name

        adjacency_settings = dict((k, settings[k]) for k in
                                  ['use_pc_1', 'use_pc_2', 'use_pc_3',
                                   'use_pc_4', 'n_pcs', ])

        f = plt.figure(figsize=(10, 10))

        plt.axis((-0.2, 1.2, -0.2, 1.2))
        main_ax = plt.gca()
        ax_pev = plt.axes([0.1, .8, .2, .15])
        ax_cov = plt.axes([0.1, 0.1, .2, .15])
        ax_degree = plt.axes([0.9, .8, .2, .15])

        pca = self.DataModel.reduce(
            # label_to_color=label_to_color,
            # label_to_marker=label_to_marker,
            # groupby=groupby,
            **pca_settings)

        if featurewise:
            node_color_mapper = lambda x: 'r' \
                if x == feature_of_interest else 'k'
            node_size_mapper = lambda x: (pca.means.ix[x] ** 2) + 10
        else:
            if sample_id_to_color is not None:
                node_color_mapper = lambda x: sample_id_to_color[x]
            else:
                node_color_mapper = lambda x: blue
            node_size_mapper = lambda x: 75

        ax_pev.plot(pca.explained_variance_ratio_ * 100.)
        ax_pev.axvline(n_pcs, label='cutoff', color=green)
        ax_pev.legend()
        ax_pev.set_ylabel("% explained variance")
        ax_pev.set_xlabel("component")
        ax_pev.set_title("Explained variance from dim reduction")
        seaborn.despine(ax=ax_pev)

        adjacency = self.adjacency(pca.reduced_space, **adjacency_settings)
        cov_dist = np.array(
            [i for i in adjacency.values.ravel() if np.abs(i) > 0])
        cov_cut = np.mean(cov_dist) + cov_std_cut * np.std(cov_dist)

        graph_settings = dict(
            (k, settings[k]) for k in ['weight_function', 'degree_cut', ])
        graph_settings['cov_cut'] = cov_cut
        this_graph_name = "_".join(map(dict_to_str,
                                       [pca_settings, adjacency_settings,
                                        graph_settings]))
        graph_settings['name'] = this_graph_name

        seaborn.kdeplot(cov_dist, ax=ax_cov)
        ax_cov.axvline(cov_cut, label='cutoff', color=green)
        ax_cov.set_title("covariance in dim reduction space")
        ax_cov.set_ylabel("density")
        ax_cov.legend()
        seaborn.despine(ax=ax_cov)

        graph, pos = self.graph(adjacency, **graph_settings)

        nx.draw_networkx_nodes(
            graph, pos,
            node_color=map(node_color_mapper, graph.nodes()),
            node_size=map(node_size_mapper, graph.nodes()),
            ax=main_ax, alpha=0.5)

        try:

            feature_id = self.DataModel.maybe_renamed_to_feature_id(
                feature_of_interest)[0]

            node_color = map(lambda x: pca.X[feature_id].ix[x], graph.nodes())

            nx.draw_networkx_nodes(graph, pos, node_color=node_color,
                                   cmap=mpl.cm.Greys,
                                   node_size=map(
                                       lambda x: node_size_mapper(x) * .5,
                                       graph.nodes()), ax=main_ax, alpha=1)
        except (KeyError, ValueError):
            pass

        if featurewise:
            namer = self.DataModel.feature_renamer
        else:
            namer = lambda x: x
        labels = dict([(name, namer(name)) for name in graph.nodes()])
        if draw_labels:
            nx.draw_networkx_labels(graph, pos, labels=labels, ax=main_ax)
        nx.draw_networkx_edges(graph, pos, ax=main_ax, alpha=0.1)
        main_ax.set_axis_off()
        degree = nx.degree(graph)
        seaborn.kdeplot(np.array(degree.values()), ax=ax_degree)
        ax_degree.set_xlabel("degree")
        ax_degree.set_ylabel("density")
        try:
            ax_degree.axvline(x=degree[feature_of_interest],
                              label=feature_of_interest)
            ax_degree.legend()

        except Exception as e:
            sys.stdout.write(str(e))
            pass

        seaborn.despine(ax=ax_degree)
        if graph_file != '':
            try:
                nx.write_gml(graph, graph_file)
            except Exception as e:
                sys.stdout.write("error writing graph file:"
                                 "\n{}".format(str(e)))

        return graph, pos

    def draw_nonreduced_graph(self,
                              degree_cut=2, cov_std_cut=1.8,
                              wt_fun='abs',
                              featurewise=False,  # else feature_components
                              rpkms_not_events=False,  # else event features
                              feature_of_interest='RBFOX2', draw_labels=True,
                              feature_ids=None,
                              group_id=None,
                              graph_file='',
                              compare=""):

        """
                Parameters
        ----------
        feature_ids : list of str, or None
            Feature ids to subset the data. If None, all features will be used.
        sample_ids : list of str, or None
            Sample ids to subset the data. If None, all features will be used.
        x_pc : str
            x component for DataFramePCA, default "pc_1"
        y_pc :
            y component for DataFramePCA, default "pc_2"
        n_pcs : int???
            n components to use for cells' covariance calculation
        cov_std_cut : float??
            covariance cutoff for edges
        use_pc{1-4} use these pcs in cov calculation (default True)
        degree_cut : int??
            miniumum degree for a node to be included in graph display
        weight_function : ['arctan' | 'sq' | 'abs' | 'arctan_sq']
            weight function (arctan (arctan cov), sq (sq cov), abs (abs cov),
            arctan_sq (sqared arctan of cov))
        gene_of_interest : str
            map a gradient representing this gene's data onto nodes (ENSEMBL
            id or gene name???)


        Returns
        -------
        #TODO: Mike please fill these in
        graph : ???
            ???
        pos : ???
            ???
        """
        node_color_mapper = self._default_node_color_mapper
        node_size_mapper = self._default_node_color_mapper
        settings = locals().copy()

        adjacency_settings = dict(('non_reduced', True))

        f = plt.figure(figsize=(10, 10))
        plt.axis((-0.2, 1.2, -0.2, 1.2))
        main_ax = plt.gca()
        ax_cov = plt.axes([0.1, 0.1, .2, .15])
        ax_degree = plt.axes([0.9, .8, .2, .15])

        data = self.DataModel.df

        if featurewise:
            node_color_mapper = lambda x: 'r' \
                if x == feature_of_interest else 'k'
            node_size_mapper = lambda x: (data.mean().ix[x] ** 2) + 10
        else:
            node_color_mapper = lambda x: \
                self.DataModel.sample_metadata.color[x]
            node_size_mapper = lambda x: 75

        adjacency_name = "_".join([dict_to_str(adjacency_settings)])
        adjacency = self.adjacency(data, name=adjacency_name,
                                   **adjacency_settings)
        cov_dist = np.array(
            [i for i in adjacency.values.ravel() if np.abs(i) > 0])
        cov_cut = np.mean(cov_dist) + cov_std_cut * np.std(cov_dist)

        graph_settings = dict(
            (k, settings[k]) for k in ['wt_fun', 'degree_cut', ])
        graph_settings['cov_cut'] = cov_cut
        this_graph_name = "_".join(
            map(dict_to_str, [adjacency_settings, graph_settings]))
        graph_settings['name'] = this_graph_name

        seaborn.kdeplot(cov_dist, ax=ax_cov)
        ax_cov.axvline(cov_cut, label='cutoff')
        ax_cov.set_title("covariance in original space")
        ax_cov.set_ylabel("density")
        ax_cov.legend()
        seaborn.despine(ax=ax_cov)
        g, pos = self.graph(adjacency, **graph_settings)

        nx.draw_networkx_nodes(g, pos,
                               node_color=map(node_color_mapper, g.nodes()),
                               node_size=map(node_size_mapper, g.nodes()),
                               ax=main_ax, alpha=0.5)
        try:
            node_color = map(lambda x: data[feature_of_interest].ix[x],
                             g.nodes())
            nx.draw_networkx_nodes(g, pos, node_color=node_color,
                                   cmap=plt.cm.Greys,
                                   node_size=map(
                                       lambda x: node_size_mapper(x) * .5,
                                       g.nodes()), ax=main_ax, alpha=1)
        except:
            pass

        nmr = lambda x: x
        labels = dict([(nm, nmr(nm)) for nm in g.nodes()])
        if draw_labels:
            nx.draw_networkx_labels(g, pos, labels=labels, ax=main_ax)
        nx.draw_networkx_edges(g, pos, ax=main_ax, alpha=0.1)
        main_ax.set_axis_off()
        degree = nx.degree(g)
        seaborn.kdeplot(np.array(degree.values()), ax=ax_degree)
        ax_degree.set_xlabel("degree")
        ax_degree.set_ylabel("density")
        try:
            ax_degree.axvline(x=degree[feature_of_interest],
                              label=feature_of_interest)
            ax_degree.legend()

        except Exception as e:
            sys.stdout.write(str(e))
            pass

        seaborn.despine(ax=ax_degree)
        if graph_file != '':
            try:
                nx.write_gml(g, graph_file)
            except Exception as e:
                sys.stdout.write("error writing graph file:"
                                 "\n{}".format(str(e)))

        return (g, pos)
