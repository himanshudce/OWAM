from river import base, cluster, utils


class STREAMKMeans(base.Clusterer):
    r"""STREAMKMeans

    STREAMKMeans is an alternative version of the original algorithm STREAMLSEARCH proposed by
    O'Callaghan et al. [^1] by replacing the `k-Medians` using `LSEARCH` by the classical
    `KMeans` algorithm.

    However, instead of using the traditional `KMeans` that requires a total reclustering after
    each time the temporary chunk of data points is full, the implementation of this algorithm
    in `River` uses the increamental `KMeans`. This allows the algorithm to update `KMeans`
    without the need of re-initialization, saving a substantial amount of computing resources.

    The algorithm is constructed as follows. To begin, the algorithm will be initialized
    with an incremental `KMeans` algorithm with the same number of centers as required.
    For a new point `p`:

    * If the size of chunk is less than the maximum size allowed, add the new point to
    the temporary chunk.

    * When the size of chunk reaches the maximum value size allowed

        - A new incremental `KMeans` algorithm will be initiated. This algorithm will run
        through all points in the temporary chunk. The centers of this new algorithm will
        be passed through the originally initialized `KMeans` to update the centers of the
        algorithm

        - All points will be deleted from the temporary chunk to continue adding new points later.

    * When a prediction request arrives, the centers of the algorithm will be exactly the same
    as the centers of the original `KMeans` at the time of retrieval.

    Parameters
    ----------
    chunk_size
        Maximum size allowed for the temporary data chunk.

    n_clusters
        Number of clusters generated by the algorithm.

    kwargs
        Other parameters passed to the incremental kmeans at `cluster.KMeans`.

    Attributes
    ----------
    centers
        Cluster centers generated from running the incremental `KMeans` algorithm
        through centers of each chunk.

    References
    ----------
    [^1]: O'Callaghan et al. (2002). Streaming-data algorithms for high-quality clustering.
          In Proceedings 18th International Conference on Data Engineering, Feb 26 - March 1,
          San Jose, CA, USA. DOI: 10.1109/ICDE.2002.994785.

    Examples
    ----------

    >>> from river import cluster
    >>> from river import stream

    >>> X = [
    ...     [1, 0.5], [1, 0.625], [1, 0.75], [1, 1.125], [1, 1.5], [1, 1.75],
    ...     [4, 1.5], [4, 2.25], [4, 2.5], [4, 3], [4, 3.25], [4, 3.5]
    ... ]

    >>> streamkmeans = cluster.STREAMKMeans(chunk_size=3, n_clusters=2, halflife=0.5, sigma=1.5, seed=0)

    >>> for x, _ in stream.iter_array(X):
    ...     streamkmeans = streamkmeans.learn_one(x)

    >>> streamkmeans.predict_one({0: 1, 1: 0})
    0

    >>> streamkmeans.predict_one({0: 5, 1: 2})
    1

    """

    def __init__(self, chunk_size=10, n_clusters=2, **kwargs):

        super().__init__()
        self.time_stamp = 0
        self.n_clusters = n_clusters
        self.chunk_size = chunk_size
        self.kwargs = kwargs

        self._kmeans = cluster.KMeans(n_clusters=self.n_clusters, **self.kwargs)
        self._temp_chunk = {}
        self.centers = {}

    def learn_one(self, x, sample_weight=None):

        self.time_stamp += 1

        index = self.time_stamp % self.chunk_size

        if index == 0:
            self._temp_chunk[self.chunk_size - 1] = x
        elif index == 1:
            self._temp_chunk = {0: x}
        else:
            self._temp_chunk[index - 1] = x

        if index == 0:
            kmeans_i = cluster.KMeans(n_clusters=self.n_clusters, **self.kwargs)
            for point_j in self._temp_chunk.values():
                kmeans_i = kmeans_i.learn_one(point_j)
            for center_j in kmeans_i.centers.values():
                self._kmeans = self._kmeans.learn_one(center_j)

        self.centers = self._kmeans.centers

        return self

    def predict_one(self, x, sample_weight=None):
        def get_distance(c):
            return utils.math.minkowski_distance(self.centers[c], x, 2)

        return min(self.centers, key=get_distance)