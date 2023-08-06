features include:
  1. order of child nodes are irrelevant  
  2. auto handling of namespace
  3. promises: not match reported <=> nonmatch exists; match reported <=> match indeed; reported nonmatch is relevant

does not support:
  1. report accurate nonmatched attributes - nonmatched nodes will be reported in this case
  2. if two nodes have different attributes, their texts will not be compared

