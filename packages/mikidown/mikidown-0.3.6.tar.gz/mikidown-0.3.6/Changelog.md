# Mikidown Changelogs

## Version 0.3.6
- Fix a confusing UI issue regarding single instance locking (clicking yes for saying mikidown's running would remove the lock, clicking no for saying mikidown's running would just quit it)
- When performing the check for nbListMigration, set a dummy version value until mikiwindow gets a chance to properly update the version strings.
- When performing the check to show the Changelog, also check the Mikibook settings string since that now also has version metadata on it.
- Make the makeExtensions config keyword have a default value of an empty dictionary because of python-markdown 2.5 details
- Instead of asciimathml as part of the default list, put mdx_asciimathml. Trying to import it without the mdx_ prefix through markdown
will result in asciimathml not being enabled.

## Version 0.3.5
- Fix a bug where there was an assault of commas in the attachmentImage and attachmentDocument settings for a mikidown notebook folder if that was edited via a dialog
- Create the attachment directory for a note if it doesn't exist
- Make attachment view use system colors
- Make attachment view scrollable horizontally
- Make attachment view's thumbnail not overflow out of the widget
- python-html2text is now an optional dependency
- Some attempts at fixing the sandbox. Link testing works, but cleaning up the sandbox under Windows doesn't work.

## Version 0.3.4
- the markdown extension configuration is also in plain text
- On that note, I also remembered to put in the markdown extension configuration in the mikidown render code this time
- Fixed a bug were the markdown extension configuration wasn't being saved correctly
- markdown extension configuration can now be used in the site generator
- The Notebook list uses system colors
- The mikidown.conf file now stores its notebooklist as pure plain text. That means you can add notebooks by editing the Ini file and it'll be able to detect them.
- The colors for mikidown markdown highlighting can be configured. There's currently no GUI for it.
- Don't force regex searching for all of the fields. Instead, allow the user to decide that. Not specifying a field defaults to searching the contents of notes. Individual fields can also be searched by typing {field_name}:expression or things like that. Surrounding expression with r"" turns on regexing for that field during search.
- Searching escaped quotes in regex searching is enabled.
- Tagging is enabled, but isn't forced. You'll need to turn on the python markdown's built in meta extension so mikidown knows what tags to give mikidown the tags you want. tags can be added by adding tags:{tag},{tag},... to the top of your note. Be sure to have a blank line between this and your actual note content. Tags can also be searched with that same syntax OR by entering tags:tagname tags:tagname2 and so on.

## Version 0.3.3
- Windows compatibility was added with making sure there's no path funkiness under Windows and swapping out forking processes for threads...because for some reason, Windows can't do the os.fork.
- markdown extensions that the user doesn't have, but has listed in their mikidown notebook config are temporarily disabled and marked in red.
- There's a GUI for configuring the markdown extensions. Just click "Edit Settings for this extension" after selecting an extension to configure.
- Single instance per user to prevent weirdness with notes. I'm currently trying to figure out how to raise the already existing window if there is one in a cross-platform manner.
- Improvements to the HTML tag detection in syntax highlighting. Now you can properly distinguish <https://github.com/rnons/mikidown> from <i>I am a block of html stuff!</i>.
- A few more fixes for setext header syntax highlighting.
- Numbered lists are included in the syntax highlighting.
- Search results can now be styled.
- Sort lines doesn't require the user to fully select lines for them to be sorted.
- The number of recently viewed notes can be adjusted by the user in the Mikidown settings dialog.

## Version 0.3.2

- asciimathml markdown extensions is supported. If you don't have it grab it from [here [AUR]](https://aur.archlinux.org/packages/python-asciimathml-git) or [here [github]](https://github.com/mtahmed/python-asciimathml)
- The MathJax javascript file by default points to the CDN. You can point it to a different place if you want.
- A dialog for configuring notebook settings has been added. You can easily change the order of how markdown uses its extensions by dragging and dropping. Disabling and enabling's also as easy as clicking a checkmark next to the corresponding item.
- Rudimentary support for highlighting asciimathml blocks is there
- There's a box in the index tab that can be used to easily access items without clicking through the note tree. Type path/to/note (where that is the path to your note) to check it out.
- Highlighting for setext style headers works too.

### Enabling asciimathml
For existing notebooks, will be autoenabled on new ones. This is for enabling it on old ones (all of this can easily be done in the notebook settings dialog too):

0. Make sure that the user has the python 3 version of [asciimathml](https://github.com/mtahmed/python-asciimathml) installed.
1. in notebookPath/notebook.conf, look for the line that says "extensions =". Add asciimathml to the end of it.
2. in notebookPath/notebook.conf, add a line that says:```mathJax = /path/to/your/MathJax.js```
For most people, pointing to the mathjax CDN mentioned below is fine:
http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML
3. Type away some asciimathml. The script pointed to in mathJax should auto-process the MathML elements spat out by asciimathml.

After following these instructions, this text //should// be processed with mathjax:

$$
sqrt 1^2^3^4
$$

### Disabling asciimathml

1. in notebookPath/notebook.conf, look for the line that says "extensions =". Remove asciimathml from it.

## Version 0.3.0

- Notebook folder redesigned, see [#23]
        // notebook.conf attachments/ css/ notes/ _site/ //

- When attachment (image or document) is inserted, it is saved into **attachment/** folder
- Spell checking support with enchant, see [#24]
        new optional dependencies: [pyenchant]

- A simple static site generator incorporated

        mikidown generate
        mikidown preview


[#23]: https://github.com/rnons/mikidown/issues/23
[#24]: https://github.com/rnons/mikidown/issues/24
[pyenchant]: https://pypi.python.org/pypi/pyenchant
