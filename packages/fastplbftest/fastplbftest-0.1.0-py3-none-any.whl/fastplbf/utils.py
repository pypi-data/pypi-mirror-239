import math
import csv
import random
import bisect
from typing import Tuple
from fastplbf.const import INF, EPS

class prList:

    def __init__(self, scores: list, thre_list: list):
        """

        Args:
            scores (list): a list of scores
            thre_list (list): thresholds for divide scores into segment

        """

        assert(thre_list[0] == 0)
        assert(thre_list[-1] == 1)

        self.thre_list = thre_list
        self.N = len(thre_list) - 1

        cnt_list = [0 for _ in range(self.N + 1)]
        for score in scores:
            assert(0 <= score <= 1)

            segment_idx = bisect.bisect_left(thre_list, score)
            if segment_idx == 0:
                assert(score == 0)
                segment_idx = 1

            assert(1 <= segment_idx <= self.N)

            cnt_list[segment_idx] += 1
        
        total_cnt = len(scores)

        self.pr = [0.0 for i in range(self.N+1)]
        self.accPr = [0.0 for i in range(self.N+1)]
        for i in range(1, self.N + 1):
            self.pr[i] = cnt_list[i] / total_cnt
            self.accPr[i] = self.accPr[i - 1] + self.pr[i]
    
        assert(abs(self.accPr[self.N] - 1.0) < EPS), self.accPr[self.N]

    def get_th_idx(self, score: float) -> int:
        """
        0 --> 0
        1/N --> 1
        2/N --> 2
        ...
        N/N --> N

        Args:
            score (float): score

        Returns:
            int: idx
        """

        idx = math.floor(score * self.N + 0.5)
        assert(abs(idx - score * self.N) < 1e-9)

        return idx


    def acc(self, score: float) -> float:
        """

        Args:
            score (float): \in [0, 1]
        Returns:
            float: accumulated probability in [0, score]
        """

        idx = self.get_th_idx(score)

        return self.accPr[idx]

        
    def acc_range(self, score_l: float, score_r: float) -> float:
        """

        Args:
            score_l (float): \in [0, 1]
            score_r (float): \in [0, 1]

        Returns:
            float: accumulated probability in [score_l, score_r]
        """

        idx_l = self.get_th_idx(score_l)
        idx_r = self.get_th_idx(score_r)

        return self.accPr[idx_r] - self.accPr[idx_l]
    
    def acc_idx(self, idx: int) -> float:
        """

        Args:
            idx (int): idx \in {1 ... N}

        Returns:
            float: sum of self.pr[1...idx]
        """
        
        assert(1 <= idx <= self.N)

        return self.accPr[idx]

    def acc_range_idx(self, idx_l: int, idx_r: int) -> float:
        """

        Args:
            idx_l (int): idx \in {1 ... N}
            idx_l (int): idx \in {1 ... N}

        Returns:
            float: sum of self.pr[idx_l...idx_r]
        """

        assert(1 <= idx_l <= self.N)
        assert(1 <= idx_r <= self.N)
        
        return self.accPr[idx_r] - self.accPr[idx_l - 1]

def calc_DPKL(g: prList, h: prList, k: int, j: int = None) -> Tuple:
    N = g.N
    if j is None:
        j = N

    DPKL = [[-INF for _ in range(k + 1)] for _ in range(j + 1)]
    DPPre = [[None for _ in range(k + 1)] for _ in range(j + 1)]
    DPKL[0][0] = 0
    for n in range(1, j + 1):
        for q in range(1, k + 1):
            for i in range(1, n + 1):
                # i-th to n-th segments are clustered into q-th region

                Pos = g.acc_range_idx(i, n)
                Neg = h.acc_range_idx(i, n)
                
                if Neg == 0:
                    continue
                if Pos == 0:
                    tmp_sum = DPKL[i-1][q-1] + 0
                else:
                    tmp_sum = DPKL[i-1][q-1] + Pos * math.log(Pos / Neg)

                if DPKL[n][q] < tmp_sum:
                    DPKL[n][q] = tmp_sum
                    DPPre[n][q] = i-1

    return DPKL, DPPre

def ExpectedFPR(g: prList, h: prList, t: list, f: list, n: int) -> float:
    """

    Args:
        g (prList): key density of each segmenet
        h (prList): non-key density of each segmenet
        t (list): threshold boundaries of each region
        f (list): FPRs of each region
        n (int): the number of keys
    Returns:
        float: expectedFPR
    """

    N = g.N
    k = len(t) - 1

    expectedFPR = 0
    for i in range(1, k+1):
        neg_pr = h.acc_range(t[i-1], t[i])
        expectedFPR += neg_pr * f[i]

    return expectedFPR

def fast_calc_DPKL(g: prList, h: prList, k: int) -> Tuple:
    """

    Args:
        g (prList): key density of each segmenet
        h (prList): non-keye density of each segmenet
        k (int): number of regions

    Returns:
        Tuple: DPKL, DPPre
    """

    N = g.N

    DPKL = [[-INF for _ in range(k + 1)] for _ in range(N + 1)]
    DPPre = [[None for _ in range(k + 1)] for _ in range(N + 1)]
    DPKL[0][0] = 0
    for j in range(1, k + 1):
        
        def func_A(p: int, i: int) -> float:
            """
            func_A(p, i) 
            = A_{pi}

            = { -INF                        (i = p+1, p+2, ..., N-1)
              { DPKL[i-1][j-1] + dkl(i, p)  (i = 1, ..., p)

            Args:
                p (int): \in {1 ... N}
                i (int): \in {1 ... N}

            Returns:
                float: A_{pi}
            """
            
            if i >= p+1:
                return -INF
            
            Pos = g.acc_range_idx(i, p)
            Neg = h.acc_range_idx(i, p)

            if Neg == 0:
                return -INF
            if Pos == 0:
                return DPKL[i-1][j-1] + 0

            return DPKL[i-1][j-1] + Pos * math.log(Pos / Neg)

        max_args = matrix_problem_on_monotone_matrix(func_A, N, N)

        for n in range(1, N + 1):
            pre = max_args[n]
            DPKL[n][j] = func_A(n, pre)
            DPPre[n][j] = pre-1

    return DPKL, DPPre

def load_csv_and_split(data_path: str, test_size = 0.7, random_state = 0) -> tuple:
    def my_train_test_split(samples, test_size, random_state):
        random.seed(random_state)
        random.shuffle(samples)
        test_size = int(len(samples) * test_size)
        train_samples = samples[test_size:]
        test_samples = samples[:test_size]
        return train_samples, test_samples

    positive_sample = []
    negative_sample = []
    with open(data_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['label'] == '1':
                positive_sample.append(row)
            else:
                negative_sample.append(row)

    train_negative, test_negative = my_train_test_split(negative_sample, test_size, random_state)

    pos_keys = []
    pos_scores = []
    train_neg_keys = []
    train_neg_scores = []
    test_neg_keys = []
    test_neg_scores = []
    
    for row in positive_sample:
        pos_keys.append(row['key'])
        pos_scores.append(float(row['score']))
    for row in train_negative:
        train_neg_keys.append(row['key'])
        train_neg_scores.append(float(row['score']))
    for row in test_negative:
        test_neg_keys.append(row['key'])
        test_neg_scores.append(float(row['score']))

    return pos_keys, pos_scores, train_neg_keys, train_neg_scores, test_neg_keys, test_neg_scores

def matrix_problem_on_monotone_matrix(f, n: int, m: int) -> list:
    
    a = [None for i in range(n + 1)]

    def CalcJ(i, jl, jr):
        max = -INF
        argmax = jl
        for j in range(jl, jr+1):
            if f(i, j) > max:
                max = f(i, j)
                argmax = j
        return argmax

    def RecSolveMP(il, ir, jl, jr):
        if il > ir:
            return
        i = math.floor((il + ir) / 2)
        j = CalcJ(i, jl, jr)
        a[i] = j
        RecSolveMP(il, i-1, jl, j)
        RecSolveMP(i+1, ir, j, jr)
    
    RecSolveMP(1, n, 1, m)
    return a
    
def OptimalFPR_M(g: prList, h: prList, t: list, M: float, k: int, n: int) -> list:
    """_summary_

    Args:
        g (prList): key density of each segmenet
        h (prList): non-keye density of each segmenet
        t (list): threshold boundaries of each region
        M (float): the target memory usage for backup Bloom filters
        k (int): number of regions
        n (int): number of keys

    Returns:
        list: FPRs of each region (1-index)
    """

    def calc_K_sum(pos_pr_list: list, neg_pr_list: list, valid_list: list) -> float:
        K_sum = 0
        for pos_pr, neg_pr, valid in zip(pos_pr_list, neg_pr_list, valid_list):
            if not valid:
                continue
            if pos_pr == 0:
                continue
            K_sum += pos_pr * math.log2(pos_pr / neg_pr)
        return K_sum

    def calc_G_sum(pos_pr_list: list, neg_pr_list: list, valid_list: list) -> float:
        G_sum = 0
        for pos_pr, neg_pr, valid in zip(pos_pr_list, neg_pr_list, valid_list):
            if valid:
                continue
            G_sum += pos_pr
        return G_sum

    def some_f_i_is_greater_than_1(f: list) -> bool:
        for f_i in f:
            if f_i > 1:
                return True
        return False


    c = math.log2(math.e)

    pos_pr_list = [g.acc_range(t[i-1], t[i]) for i in range(1, k+1)]
    neg_pr_list = [h.acc_range(t[i-1], t[i]) for i in range(1, k+1)]

    assert(abs(sum(pos_pr_list) - 1) < EPS)
    assert(abs(sum(neg_pr_list) - 1) < EPS)

    valid_list = [True for i in range(k)]

    for i in range(k):
        if neg_pr_list[i] == 0:
            valid_list[i] = False

    G_sum = calc_G_sum(pos_pr_list, neg_pr_list, valid_list)
    K_sum = calc_K_sum(pos_pr_list, neg_pr_list, valid_list)

    beta = (M + c * n * K_sum) / (c * n * (1 - G_sum))

    opt_fpr_list = [0 for i in range(k)]
    for i in range(k):
        if not valid_list[i]:
            opt_fpr_list[i] = 1
        else:
            opt_fpr_list[i] = math.pow(2, -beta) * pos_pr_list[i] / neg_pr_list[i]

    while some_f_i_is_greater_than_1(opt_fpr_list):
        for i in range(k):
            if opt_fpr_list[i] > 1:
                valid_list[i] = False
                opt_fpr_list[i] = 1

        G_sum = calc_G_sum(pos_pr_list, neg_pr_list, valid_list)
        K_sum = calc_K_sum(pos_pr_list, neg_pr_list, valid_list)

        beta = (M + c * n * K_sum) / (c * n * (1 - G_sum))

        for i in range(k):
            if not valid_list[i]:
                opt_fpr_list[i] = 1
            else:
                opt_fpr_list[i] = math.pow(2, -beta) * pos_pr_list[i] / neg_pr_list[i]


    # f to 1-index
    opt_fpr_list.insert(0, None)

    assert(len(opt_fpr_list) == k+1)
    return opt_fpr_list

def OptimalFPR(g: prList, h: prList, t: list, F: float, k: int) -> list:
    """_summary_

    Args:
        g (prList): key density of each segmenet
        h (prList): non-keye density of each segmenet
        t (list): threshold boundaries of each region
        F (float): target overall fpr
        k (int): number of regions

    Returns:
        list: FPRs of each region (1-index)
    """


    N = g.N

    pos_pr_list = [g.acc_range(t[i-1], t[i]) for i in range(1, k+1)]
    neg_pr_list = [h.acc_range(t[i-1], t[i]) for i in range(1, k+1)]

    assert(abs(sum(pos_pr_list) - 1) < EPS)
    assert(abs(sum(neg_pr_list) - 1) < EPS)

    valid_list = [True for i in range(k)]

    for i in range(k):
        if neg_pr_list[i] == 0:
            valid_list[i] = False

    while True:
        valid_pos_pr_sum = 0
        valid_neg_pr_sum = 0
        invalid_pos_pr_sum = 0
        invalid_neg_pr_sum = 0
        for val, pos_pr, neg_pr in zip(valid_list, pos_pr_list, neg_pr_list):
            if val:
                valid_pos_pr_sum += pos_pr
                valid_neg_pr_sum += neg_pr
            else:
                invalid_pos_pr_sum += pos_pr
                invalid_neg_pr_sum += neg_pr
        normed_F = (F - invalid_neg_pr_sum) / (1 - invalid_neg_pr_sum)

        if valid_pos_pr_sum == 0:
            # The F is too large that the Bloom filter does not need to be used.
            opt_fpr_list = []
            for i in range(k):
                if valid_list[i]:
                    opt_fpr_list.append(0.0)
                else:
                    opt_fpr_list.append(1.0)
            # f to 1-index
            opt_fpr_list.insert(0, None)

            return opt_fpr_list

        normed_pos_pr_list = [0 for i in range(k)]
        normed_neg_pr_list = [0 for i in range(k)]
        for idx, (pos_pr, neg_pr) in enumerate(zip(pos_pr_list, neg_pr_list)):
            if valid_list[idx]:
                normed_pos_pr_list[idx] = pos_pr / valid_pos_pr_sum
                normed_neg_pr_list[idx] = neg_pr / valid_neg_pr_sum

        opt_fpr_list = [0 for i in range(k)]
        for idx, (n_pos_pr, n_neg_pr) in enumerate(zip(normed_pos_pr_list, normed_neg_pr_list)):
            if not valid_list[idx]:
                opt_fpr_list[idx] = 1
            else:
                opt_fpr_list[idx] = normed_F * n_pos_pr / n_neg_pr

        ok = True
        for idx, opt_fpr in enumerate(opt_fpr_list):
            if opt_fpr > 1:
                ok = False
                valid_list[idx] = False
        if ok:
            break

    # f to 1-index
    opt_fpr_list.insert(0, None)

    assert(len(opt_fpr_list) == k+1)
    return opt_fpr_list

def SpaceUsed(g: prList, h: prList, t: list, f: list, n: int) -> float:
    """

    Args:
        g (prList): key density of each segmenet
        h (prList): non-keye density of each segmenet
        t (list): threshold boundaries of each region
        f (list): FPRs of each region
        n (int): the number of keys
    Returns:
        float: spaceUsed
    """

    N = g.N
    k = len(t) - 1

    spaceUsed = 0
    for i in range(1, k+1):
        pos_pr = g.acc_range(t[i-1], t[i])
        pos_num = pos_pr * n
        if pos_num == 0:
            continue
        fpr = f[i]
        hash_num = math.log(fpr) / math.log(0.5)
        m = hash_num * pos_num / math.log(2)
        spaceUsed += m

    return spaceUsed

def ThresMaxDivDP(g: prList, h: prList, j: int, k: int) -> list:
    """

    Args:
        g (prList): key density of each segmenet
        h (prList): non-keye density of each segmenet
        j (int): j-th to N-th segments are clustered as k-th region
        k (int): number of regions

    Returns:
        list: t (threshold boundaries of each region)
    """

    assert(isinstance(g, prList))
    assert(isinstance(h, prList))
    assert(isinstance(j, int))
    assert(isinstance(k, int))
    N = g.N
    assert(h.N == N)


    DPKL, DPPre = calc_DPKL(g, h, k, j)

    #  tracing the transitions backward from DPPre[j-1][k-1]
    if DPPre[j-1][k-1] is None:
        return None

    reversed_t = [1.0]

    now = j-1
    reversed_t.append(g.thre_list[now])
    for i in reversed(range(1, k)):
        now = DPPre[now][i]
        reversed_t.append(g.thre_list[now])
    
    t = list(reversed(reversed_t))

    assert(len(t) == k+1)
    return t

def MaxDivDP(g: prList, h: prList, N: int, k: int) -> Tuple:
    """

    Args:
        g (prList): key density of each segmenet
        h (prList): non-keye density of each segmenet
        N (int): number of segments
        k (int): number of regions

    Returns:
        Tuple: DPKL, DPPre
    """

    assert(isinstance(g, prList))
    assert(isinstance(h, prList))
    assert(isinstance(N, int))
    assert(isinstance(k, int))
    N = g.N
    assert(h.N == N)

    DPKL, DPPre = calc_DPKL(g, h, k)
    return DPKL, DPPre

def ThresMaxDiv(DPPre, j: int, k: int, thre_list: list):
    """

    Args:
        DPPre (): DPPre
        j (int): j-th to N-th segments are clustered as k-th region
        k (int): number of regions
    """

    assert(isinstance(DPPre, list))
    assert(isinstance(j, int))
    assert(isinstance(k, int))
    
    # tracing the transitions backward from DPPre[j-1][k-1]
    if DPPre[j-1][k-1] is None:
        return None

    reversed_t = [1.0]

    now = j-1
    reversed_t.append(thre_list[now])
    for i in reversed(range(1, k)):
        now = DPPre[now][i]
        if now is None:
            return None
        reversed_t.append(thre_list[now])
    
    t = list(reversed(reversed_t))

    assert(len(t) == k+1)
    return t

def fastMaxDivDP(g: prList, h: prList, N: int, k: int) -> Tuple:
    """

    Args:
        g (prList): key density of each segmenet
        h (prList): non-keye density of each segmenet
        N (int): number of segments
        k (int): number of regions

    Returns:
        Tuple: DPKL, DPPre
    """

    N = g.N

    DPKL, DPPre = fast_calc_DPKL(g, h, k)
    return DPKL, DPPre

