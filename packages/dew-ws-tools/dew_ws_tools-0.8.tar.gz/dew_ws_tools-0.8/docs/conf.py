project = 'dew_ws_tools'

copyright = '2022, DEW Water Science'
author = 'Kent Inverarity'


from pkg_resources import get_distribution

project_name = "dew_ws_tools"
release = get_distribution(project_name).version
# version = ".".join(release.split(".")[:2])
version = release

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.ifconfig",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx.ext.napoleon",
    "nbsphinx",
]

templates_path = ["_templates"]

source_suffix = ".rst"
master_doc = "index"
language = None

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
pygments_style = None

html_theme = "sphinx_rtd_theme"

html_theme_options = {
    "icon_links": [
        {
            "name": "GitHub",
            "url": f"https://github.com/dew-waterscience/{project_name}",
            "icon": "fab fa-github",
        },
    ],
    "show_nav_level": 2,
    "show_toc_level": 2,
    "use_edit_page_button": True,
    "navbar_start": ["navbar-logo"],
    # "navbar_center": ["navbar-nav"],
    "navbar_center": [],
    "navbar_end": ["navbar-icon-links"],
}

html_context = {
    # "github_url": "https://github.com", # or your self-hosted GitHub
    "github_user": "dew-waterscience",
    "github_repo": project_name,
    "github_version": "main",
    "doc_path": "docs",
}

html_static_path = ["_static"]

html_css_files = [
    "css/custom.css",
]


html_sidebars = {
    # "**": ["search-field", "sidebar-nav-bs", "sidebar-ethical-ads"]
    # "**": ["search-field", "sidebar-nav-bs",]
    "**": [
        "search-field",
        "navbar-nav",
        "parent_links",
    ]
}



# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

True


def setup(app):
    app.add_css_file("custom.css")
