from fastplbf.utils import ThresMaxDivDP, OptimalFPR_M, SpaceUsed, prList, load_csv_and_split, ExpectedFPR, MaxDivDP, ThresMaxDiv, fastMaxDivDP
from fastplbf.const import INF
from fastplbf.PLBF_M import PLBF_M

import time
import argparse

class FastPLBF_M(PLBF_M):
    def __init__(self, pos_keys: list, pos_scores: list, neg_scores: list, M: float, N: int, k: int):
        """
        Args:
            pos_keys (list): keys
            pos_scores (list): scores of keys
            neg_scores (list): scores of non-keys
            M (float): the target memory usage for backup Bloom filters
            N (int): number of segments
            k (int): number of regions
        """

        # assert 
        assert(isinstance(pos_keys, list)), f"pos_keys type must be list, but got {type(pos_keys)}"
        assert(isinstance(pos_scores, list)), f"pos_scores type must be list, but got {type(pos_scores)}"
        assert(len(pos_keys) == len(pos_scores)), f"len(pos_keys) must be equal to len(pos_scores), but got {len(pos_keys)} and {len(pos_scores)}"
        assert(isinstance(neg_scores, list)), f"neg_scores type must be list, but got {type(neg_scores)}"
        assert(isinstance(M, float) or isinstance(M, int)), f"M type must be float or int, but got {type(M)}"
        assert(0 < M), f"M must be positive, but got {M}"
        assert(isinstance(N, int)), f"N type must be int, but got {type(N)}"
        assert(isinstance(k, int)), f"k type must be int, but got {type(k)}"

        for score in pos_scores:
            assert(0 <= score <= 1), f"pos_scores must be in [0, 1], but got {score}"
        for score in neg_scores:
            assert(0 <= score <= 1), f"neg_scores must be in [0, 1], but got {score}"


        
        self.M = M
        self.N = N
        self.k = k
        self.n = len(pos_keys)

        
        segment_thre_list, g, h = self.divide_into_segments(pos_scores, neg_scores)
        self.find_best_t_and_f(segment_thre_list, g, h)
        self.insert_keys(pos_keys, pos_scores)
        
    def find_best_t_and_f(self, segment_thre_list, g, h):
        minExpectedFPR = INF
        t_best = None
        f_best = None

        DPKL, DPPre = MaxDivDP(g, h, self.N, self.k)
        for j in range(self.k, self.N+1):
            t = ThresMaxDiv(DPPre, j, self.k, segment_thre_list)
            if t is None:
                continue
            f = OptimalFPR_M(g, h, t, self.M, self.k, self.n)
            if minExpectedFPR > ExpectedFPR(g, h, t, f, self.n):
                minExpectedFPR = ExpectedFPR(g, h, t, f, self.n)
                t_best = t
                f_best = f

        self.t = t_best
        self.f = f_best
        self.memory_usage_of_backup_bf = SpaceUsed(g, h, t, f, self.n)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', action="store", dest="data_path", type=str, required=True,
                        help="path of the dataset")
    parser.add_argument('--N', action="store", dest="N", type=int, required=True,
                        help="N: the number of segments")
    parser.add_argument('--k', action="store", dest="k", type=int, required=True,
                        help="k: the number of regions")
    parser.add_argument('--M', action="store", dest="M", type=float, required=True,
                        help="M: the target memory usage for backup Bloom filters")

    results = parser.parse_args()

    DATA_PATH = results.data_path
    N = results.N
    k = results.k
    M = results.M

    pos_keys, pos_scores, train_neg_keys, train_neg_scores, test_neg_keys, test_neg_scores = load_csv_and_split(DATA_PATH, test_size = 0.7, random_state = 0)

    construct_start = time.time()
    plbf = FastPLBF_M(pos_keys, pos_scores, train_neg_scores, M, N, k)
    construct_end = time.time()

    # assert : no false negative
    for key, score in zip(pos_keys, pos_scores):
        assert(plbf.contains(key, score))
    
    # test
    fp_cnt = 0
    for key, score in zip(test_neg_keys, test_neg_scores):
        if plbf.contains(key, score):
            fp_cnt += 1
    
    print(f"Construction Time: {construct_end - construct_start}")
    print(f"Memory Usage of Backup BF: {plbf.memory_usage_of_backup_bf}")
    print(f"False Positive Rate: {fp_cnt / len(test_neg_keys)} [{fp_cnt} / {len(test_neg_keys)}]")


