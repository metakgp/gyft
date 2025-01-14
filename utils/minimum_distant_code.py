from timetable.course_data import course_code_map

def levenshtein_distance(str1, str2, m, n):
  if m == 0:
    return n
  if n == 0:
    return m
  if str1[m - 1] == str2[n - 1]:
    return levenshtein_distance(str1, str2, m - 1, n - 1)
  return 1 + min(     
    levenshtein_distance(str1, str2, m, n - 1),
    levenshtein_distance(str1, str2, m - 1, n),
    levenshtein_distance(str1, str2, m - 1, n - 1)
  )

def jaccard_similarity(s1, s2, n=2):
    ngrams1 = set([s1[i:i+n] for i in range(len(s1)-n+1)])
    ngrams2 = set([s2[i:i+n] for i in range(len(s2)-n+1)])
    intersection = len(ngrams1 & ngrams2)
    union = len(ngrams1 | ngrams2)
    return intersection / union


def get_minimum_distant_code(code: str) -> str:
  if code in course_code_map:
    return code
  max_d, max_d_str = 0, ""
  for k, v in course_code_map.items():
      l_d = jaccard_similarity(code, k)
      if(l_d >= max_d):
          max_d = l_d
          max_d_str = k
  return max_d_str