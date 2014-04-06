# CSS Parser

This is a a CSS modeling utility written in pure Python. 

## Features

### StyleSheet

1. [✓] Create from file
2. [✓] Create from string
3. [✓] Write to file
4. [✓] Write to string
5. [✓] Get rules by query string
6. [✓] Remove rule
7. [✓] Prepend rule
8. [✓] Append rule
9. [✓] Add rule before existing rule
10. [✓] Add rule after existing rule
11. [ ] Comment out rule
12. [✓] Add rule to media-query
13. [ ] Add rule with new media-query

### Rule

1. [✓] Create Rule from string
2. [✓] Create multiple rules from a string
1. [✓] Write Rule to string
1. [✓] Get declarations by property
1. [✓] Remove declaration
2. [✓] Append declaration
3. [ ] Prepend declaration
4. [ ] Add declaration before/after existing declaration
5. [ ] Comment out declaration



## Dependencies

It has no dependencies outside of the Python standard library. 



## Python Version

Developed and tested in v2.7.5.



## Usage ##

### StyleSheet ###

```python
from css_parser.stylesheet import StyleSheet

# parse css string
text = 'body {margin:0;} p.indent{text-indent:1em;}'
stylesheet = StyleSheet.from_string(text)

# parse css file
stylesheet = StyleSheet.from_file('path/to/css/file.css')

# write to string
txt = stylesheet.to_string()

# write to file
stylesheet.to_file('path/to/css/file.css')

# get all rules
allrules = stylesheet.get_rules()

# get rules by query
somerules = stylesheet.get_rules('p.indent')

# remove rule
stylesheet.remove_rule(rule)

# append rule
stylesheet.append_rule(newrule)

# append rule after existing rule
stylesheet.append_rule(newrule, existingrule)

# prepend rule
stylesheet.prepend_rule(newrule)

# prepend rule before existing rule
stylesheet.prepend_rule(newrule, existingrule)

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

### Rule ###

```python
from css_parser.rule import Rule

# create rule from string
text = 'blockquote {margin:1em 5% 1em 5%;}'
rule = Rule.from_string(text)

# media-queries are retained
text = '@media all {blockquote {margin:1em 5% 1em 5%;} }'
rule = Rule.from_string(text)

# multiple rules can be generated in this way, if desired
text = '/* multiple rules */' \
	'@media all {' \
	'	blockquote {' \
	'		margin:1em 5% 1em 5%;' \
	'	}' \
	'	p {' \
	'		color:blue;' \
	'	}' \
	'}'
rule = Rule.from_string(text)

'''
Note: If it is important that comments and whitespace be
preserved, use StyleSheet.from_string() rather than Rule.from_string().
'''

# write single rule to string
# includes media-query, if applicable
rule.to_string()

# get all declarations
alldeclarations = rule.get_declarations()

# get declarations by query
somedeclarations = rule.get_declarations('margin')

# remove declaration
rule.remove_declaration(declaration)

# append declaration
rule.append_declaration(declaration)
```	

### Declaration ###

```python
from css_parser.rule import Rule

# create declaration from string
text = 'margin:1em 5% 1em 5%;'
declaration = Declaration.from_string(text)
```