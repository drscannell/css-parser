# CSS Parser

This is a a CSS modeling utility written in pure Python. 

## Features

### StyleSheet

1. [✓] Create from file
2. [✓] Create from string
3. [✓] Write to file
4. [✓] Write to string
5. [✓] Get rules by query string > `stylesheet.get_rules('.indent')`
6. [✓] Remove rule
7. [ ] Prepend rule
8. [✓] Append rule
9. [✓] Add rule before existing rule > `stylesheet.insert_rule_before(newrule, existingrule)`
10. [✓] Add rule after existing rule > `stylesheet.insert_rule_after(newrule, existingrule)`
11. [ ] Comment out rule
12. [✓] Add rule to media-query

### Rule

1. [ ] Get declarations by property
2. [ ] Append declaration
3. [ ] Prepend declaration
4. [ ] Add declaration before/after existing declaration
5. [ ] Comment out declaration

## Dependencies

It has no dependencies outside of the Python standard library. 

## Python Version

Developed and tested in v2.7.5.
