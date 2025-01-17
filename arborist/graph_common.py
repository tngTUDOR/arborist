from .filesystem import write_graph
from pathlib import Path
from rdflib import Literal, RDF, URIRef, Namespace, Graph
from rdflib.namespace import DC, RDFS, OWL, FOAF, XSD, SKOS
import datetime


class CommonNamespaces:
    def __init__(self):
        self.nb = Namespace("http://ontology.bonsai.uno/core#")
        self.owltime = Namespace("https://www.w3.org/TR/owl-time/")
        self.vann = Namespace("http://purl.org/vocab/vann/")
        self.dt = Namespace("http://purl.org/dc/dcmitype/")


NS = CommonNamespaces()


def add_common_elements(graph, base_uri, title, description, author, version):
    """Add common graphs binds (abbreviations for longer namespaces) and a ``Dataset`` element.

    Input arguments:

    * ``graph``: A ``rdflib.Graph`` object
    * ``base_uri``: A string URI. Must end with ``/``.
    * ``title``, ``description``, ``author``, ``version``: Strings describing the relevant properties.

    Returns the modified graph.

    """
    if not base_uri.endswith("/"):
        raise ValueError("`base_uri` must end with '/'")

    graph.bind("bont", "http://ontology.bonsai.uno/core#")
    graph.bind("dc", DC)
    graph.bind("foaf", FOAF)
    graph.bind("xsd", XSD)
    graph.bind("owl", OWL)
    graph.bind("skos", SKOS)
    graph.bind("ot", "https://www.w3.org/TR/owl-time/")
    graph.bind("dtype", "http://purl.org/dc/dcmitype/")

    node = URIRef(base_uri)
    graph.add((node, RDF.type, NS.dt.Dataset))
    graph.add((node, DC.title, Literal(title)))
    graph.add((node, DC.description, Literal(description)))
    graph.add((node, FOAF.homepage, URIRef(base_uri + "documentation.html")))
    graph.add((node, NS.vann.preferredNamespaceUri, URIRef(base_uri + "#")))
    graph.add((node, OWL.versionInfo, Literal(version)))
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    graph.add((node, DC.modified, Literal(today, datatype=XSD.date)))
    graph.add((node, DC.publisher, Literal("bonsai.uno")))
    graph.add((node, DC.creator, URIRef("http://bonsai.uno/foaf/bonsai.rdf#bonsai")))
    graph.add((node, DC.contributor, Literal(author)))
    graph.add(
        (
            node,
            URIRef("http://creativecommons.org/ns#license"),
            URIRef("http://creativecommons.org/licenses/by/3.0/"),
        )
    )

    return graph


def generate_generic_graph(
    output_base_dir,
    kind,
    data,
    directory_structure,
    title,
    description,
    author,
    version,
    custom_binds=None,
):
    """Generate a complete ``Turtle`` file describing a specific set of graph metadata.

    Input args:

    * ``output_base_dir``: String or ``Path``. Starting output directory where subdirectories and files will be created.
    * ``kind``: String. The type of objects to be created. See below for details.
    * ``data``: A list of ``("label", "uri_suffix", "")``. See notes below.
    * ``directory_structure``: A list of subdirectory names. If ``kind`` is a string, shouldn't contain the ``kind``. E.g. ``['lcia', 'climate_change']``.
    * ``title``: String.
    * ``description``: String.
    * ``author``: String.
    * ``version``: String.
    * ``custom_binds``: TODO

     **``kind``**

    The valid BONSAI string types are:

    * ``ActivityType``
    * ``FlowObject``
    * ``Location``
    * ``Unit``

    **``data``**

    Provided ``data`` must include the ``label``. ``uri_suffix`` is optional, and can be inferred via ``label.lower().replace(" ", "_")``.

    Generates and writes the turtle file. Returns nothing.

    """
    BASE_TYPES = {
        "ActivityType": "brdfat",
        "FlowObject": "brdffo",
        "Location": "brdflo",
        "Unit": "brdfun",
    }

    if kind not in BASE_TYPES:
        raise ValueError("{} not in BONSAI base ontology types".format(kind))

    output_base_dir = Path(output_base_dir)

    base_uri = (
        "http://rdf.bonsai.uno/"
        + kind.lower()
        + "/"
        + "/".join(directory_structure)
        + "/"
    )

    g = add_common_elements(
        graph=Graph(),
        base_uri=base_uri,
        title=title,
        description=description,
        author=author,
        version=version,
    )

    lns = Namespace(base_uri)
    g.bind(BASE_TYPES[kind], base_uri)

    if custom_binds:
        for k, v in custom_binds.items():
            g.bind(k, v)

    for line in data:
        label = line[0]
        if len(line) == 1:
            uri = lns[line[0].lower().replace(" ", "_")]
        else:
            uri = lns[line[1]]
        if len(line) > 2:
            type_ = line[2]
        else:
            type_ = NS.nb[kind]

        node = URIRef(uri)
        g.add((node, RDF.type, type_))
        g.add((node, RDFS.label, Literal(label)))

    output_dir = output_base_dir
    if isinstance(kind, str):
        output_dir = output_dir / kind.lower()
    for subdir in directory_structure:
        output_dir = output_dir / subdir

    write_graph(output_dir, g)
