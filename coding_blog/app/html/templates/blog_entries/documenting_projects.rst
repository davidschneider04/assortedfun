Code Knowledge Brain Dump
==============================

first of all, you should know :term:`hoopoo`

Python packages:
    
At their core, these are just python files that save been structured a special way to make them more extendable.

We first add some scaffolding that lets python know we should be able to import the code as a module. This is the __init__ file, ours is blank which is fine.

Then we create the setup.py file, which is copied from some template I found and thus largely the same for all my modules with just the basic descriptors swapped out. What this does is give pip instructions of how the library should be installed into the environment it's running in. This of course involves moving the package contents to the environment's lib/site-packages/ folder so that scripts can call "import X" from any location, but we can also add extra instructions like "also install A, B, and C". At one point I had things set up to copy over credential files and stuff, but it doesn't seem to work much.

With this structure created, we have the minimum template required for an installable package. As always, we can manage its installation via Package Installer for Python (pip). Like other languages' package managers, pip takes instructions pointing to a package and attempts to install it. By default, it assumes it should be looking in the pypi.org repository, which is a pretty good bet for most reputable packages that we will anticipate needing. But since we don't want to share our work with others, we will just skip any sort of "nickname" lookup and just point explicitly at what we want. The beginning of the command remains the same. If the package is for example hosted in a git repository, we can tell pip as such:

pip install -U git+https://{$USER}:{$PW}@gitlab.com/nameofyourpackage.git

(Extra) As we so enthusiastically conversed about earlier, this tells Python it needs to run the setup.py file presumably contained within nameofyourpackage.git. More precisely, it tells the system to use the best installation method available given the operating system and Python version being used. One of the hurdles we still haven't addressed is if our package uses or depends on code from languages that require compilation. This will be a necessary step in the installation process because our internals first need to understand our operating system and version to then judge how that compilation should occur. If we were more ambitious, we could anticipate these situations (realistically, have another third party figure out the combinations that we need for us), run the compilations ourselves, then zip everything up into a speedy pre-customized "wheel" file. This also removes the need to involve other tools like GCC which can require elevated privileges since we are skipping the part that we need them for. Regardless, you should be able to make a perfectly fine package without these if you want.

The -U ensures we get the most recent version. Just like cloning, if you desire a specific commit you just need to include it in the target:



Hack the planet! We now have an easily installable package that works just like your favorite celebrities like pandas, sklearn, etc.
W


Sphinx: A language/framework specifically for documenting other languages/frameworks. Sphinx takes your project's code and other files, then combines them all together to create documentation in whatever format we need. If we have Sphinx in our project's environment (`pip install sphinx`), running the following from the root docs/ folder will create/update our documentation:

```make clean html``` "Make" is our command for Sphinx to combine .py, .rst, .sql, etc. files into 1 format, which we specify as `html`. "clean" overwrites anything already there. The final html files created by Sphinx use the project content as a base combined with options and extensions configurable via the code specific to Sphinx. For example, you may have noticed that a lot of official documentation for various unrelated Python libraries looks stylistically similar. This is probably because they are all using Sphinx, and they are probably using the same theme, which dictates styling and layout options. You can see for yourself by examining the files in your `docs/themes/` folder. One example I and many others use is Read The Docs, which typically looks something like this:



While you don't necessarily need a theme, it is definitely a good idea. What you do need is the result of `make`, which is your formatted (html) documentation in a `docs/_build` folder. These will the files you eventually serve via Flask or whatever framework you choose if you want to host your documentation online. At this point it is usually a good idea to update your code repository if you are satisfied with the `make` result.


Automodule Documentation
One of the reasons Sphinx is so widely used is because programmers do not enjoy documenting their work and so prefer solutions with minimal overhead. Enter `automodule`, which delivers on its promise of perfectly acceptable documentation created without a developer's input as long as they adhere to docstring https://peps.python.org/pep-0257/ and .rst https://peps.python.org/pep-0012/ syntax. By leveraging this system, we can integrate our comments in our .py files with anything else we may be combining together with `make`. One of the best parts about this is that as long as we can successfully run `make`, our documentation will always be up to date with our most recent commit.

`docs/index.rst`
This is the most important single file when creating documentation with Sphinx. It is a master index (duh) of all your project's content and how it should be catalogued. When I say all content, I really mean it! Unless you explicitly tell Sphinx that you intend to ignore a file, it will raise a warning if it thinks it is leaving something out of the overall documentation. Most indexes will make use of a `toctree`, which is an example of a Sphinx directive https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html to extend systematic functionality on top of basic .rst style syntax.

"It's turtles all the way down".
What if we are so illustrious that we have multiple repositories whose documentation we'd like to host all in one location? Submodules to the rescue!




Git
Quick Start

0) Prerequisite: install git
```apt install git```
- If you receive "apt not found", run the command ```cat /etc/*-release``` then Google  its result plus " package manager". Then replace "apt" with the internet's advice.
- If you are running Windows, install Gentoo.

1) Initialize the git repo
1.1) Navigate to your project root:
```cd /home/{username}/{projectpath}```
1.2) run command ```git init``

2) Keep it clean with .gitignore
2.1) In your project root, create a file using Vim or whatever text editor you prefer named `.gitignore`. Any files labeled here will be omitted from your git repository tracking. A good starting point is usually:

# unimportant temp files
*__pycache__*
# virtual environment
environment/*
# any other password files as necessary
*credentials*


3) Create a checkpoint 
3.1) Tell git you are ready to save all files not contained in .gitignore with ```git add -A```
3.2) Make sure your project snapshot looks as expected by checking what files have been staged for saving: ```git status```
3.3) If you are ready to save the state of your project to its timeline, do so with ```git commit -m "you can put whatever you want as a note here"```. The value in quotations is just a note that you leave for yourself and others to give the point in your timeline a name.

4) Back things up on the internet
4.1) Create an account on GitHub/GitLab or any other online Git hosting service. In this example we will use GitHub.
4.2)  Create a link from your local repository to a subdomain within your account that we will create soon. Make sure it does not already exist so that we know we have permission and won't overwrite anything. Then:
```git remote add origin master```
If you receive the error "<<ADD THIS SHIT IN>>", find the name of your repository default branch with <<ALSO THIS>> then change "master" to that output in that and any further commands.
4.3) Synchronize the state of your current local repository copy with the internet link you just created:
```git push origin master```.

5) Keep the party going
5.1) Work on your project as needed, then repeat steps 3 and 4.3 to save work.

6) What if I party too hard and mess up?
- To remove local changes and have your files look like they did when you did your last commit:
<<ALSO THIS>>
- To reset your project to how it was some point further back in time:
```# find the commit you want
git log```
Then, recreate your project as it was then:
<<ALSO THIS>>


Flask
Flask is a web framework for creating fully functional web applications entirely with Python. Unlike other web frameworks such as Django, Flask itself is as minimal as possible and does not come "batteries included". Instead, Flask entrusts the community to develop and promote their own microservices according to their framework. The developers then make their own decisions based on how they see these open source microservices work out for anyone choosing to use them. In reality, there tend to end up being only a few popular microservices for each individual niche and level of need. For example, there may be 2 relatively popular microservices focused on providing a way for visitors to leave comments. One does so extremely easily but doesn't allow for more customization, another requires more setup but provides more power-- you can see how both would become popular in their own right. <<ADD ACTUAL EXAMPLE>>

Our Flask application is a Python process just like anything else. We kick it off by running the __init__.py script. Amongst other things, this tells the system to establish an open channel for communication (a ```port```), then assign (```bind```) our application as a listener for anyone who attempts to establish contact with that channel. By combining the port with the IP address our application is running on, we have a unique address route that we can use as a spot for our application to talk with users. As long as we have permission <<ADD LINK>>, we can open more ports and bind more applications to them. This allows us to host multiple independent applications under one server, much like many independent apartments can exist within one building. Once we have an established path to our application we can also connect it to any domains we have registered on the World Wide Web using both a name registrar (I use Google Domains) and a DNS handler (I use DNSExit.com). That way people can talk to something that makes sense with whatever your Flask application does, like www.teachmylizardtorollerblade.com





One of the complaints about Python you may be most familiar with is that it is slow. Furthermore, the Python language is also not the HyperText Markup Language (HTML) that web browsers speak, so we also slow things down by needing to translate between the two. Wouldn't it be nice if we had something that could do both and have translated conversations on behalf of our Flask application? This client in between both languages is in general known as `middleware`, and the one I specifically use with Flask is called `waitress`.
