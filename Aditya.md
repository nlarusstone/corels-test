# Projects for Aditya

## Website
- [ ] Fix optimal rule list error caused by back button
- [ ] Clean up style of website
- [ ] Add logging output toggles and display to website
- [ ] Display rule list in such a way that users can interact with it and see how accuracy changes as they rearrange rules

## Code
- [ ] Turn verbosity/logging into a bit vector so it can be more finely turned on or off
Or in more C++ style, a collection of booleans which are carried around in a global structure that keeps track of the current configuration.

- - Categorize current debug messages in the code

- - Default for the web front end should be some kind of status bar (i.e., give feedback that something is happening)

- - Add command line option capability, something like -debug=log,all,none,progress,... [ideally some small number]

- - Modify the code to use booleans mapping to the command line; gather the booleans into a single global structure (that might also contain things like the current logger, etc).

- - Map the booleans to user-friendly checkboxes on the web page (we can argue about whether log should be default or not)


## Visualization
- [ ] Come up with visualization to show progress of algorithm as it runs

## Port code to R
- [ ] Write an R interface for our code (or python if you want to swap with Vassilios)
