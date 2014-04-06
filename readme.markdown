# CSS Parser

This is a a CSS modeling utility written in pure Python. 

## Usage ##

```python
# parse css string
stylesheet = StyleSheetReader.read_string('body {margin:0;} p.indent{text-indent:1em;}')

# parse css file
stylesheet = StyleSheetReader.read_filepath('path/to/css/file.css')

# write to string
txt = StyleSheetWriter.write_string(stylesheet)

# write to file
StyleSheetWriter.write_filepath(stylesheet, 'path/to/css/file.css')

# get all rules
allrules = stylesheet.get_rules()

# get rules by query
somerules = stylesheet.get_rules('p.indent')

# remove rule
stylesheet.remove_rule(rule)

# append rule
stylesheet.append(newrule)

# append rule after existing rule
stylesheet.append(newrule, existingrule)

# prepend rule
stylesheet.prepend(newrule)

# prepend rule before existing rule
stylesheet.prepend(newrule, existingrule)

# insert rule into media-query
mediaquery = existingrule.get_mediaquery()
newrule.set_mediaquery(mediaquery)
stylesheet.append(newrule, mediaquery)
'''
If the media-queries don't match, the new rule 
will be added before/after the media-query, 
depending on whether prepend_rule or 
append_rule is used.
'''
```	
	
## Features

### StyleSheet

1. [✓] Create from file
2. [✓] Create from string
3. [✓] Write to file
4. [✓] Write to string
5. [✓] Get rules by query string > `stylesheet.get_rules('.indent')`
6. [✓] Remove rule
7. [✓] Prepend rule
8. [✓] Append rule
9. [✓] Add rule before existing rule > `stylesheet.insert_rule_before(newrule, existingrule)`
10. [✓] Add rule after existing rule > `stylesheet.insert_rule_after(newrule, existingrule)`
11. [ ] Comment out rule
12. [✓] Add rule to media-query
13. [ ] Add rule with new media-query

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
