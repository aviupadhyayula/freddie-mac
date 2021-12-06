ATTRIBUTE_NORM_MAP = {
    "Verkehrsflaeche_ID": "VerkehrsflaecheID",
    "VorkehrungBepflanzungOeffentlicheVerkehrsflaeche": "VorkehrungBepflanzung",
    "AnBaulinie": "AnFluchtlinie",
    "AnStrassenfluchtlinie": "AnFluchtlinie",
    "Bauklasse_ID": "Bauklasse",
    "HochhausUnzulaessigGemaessBB": "HochhausZulaessigGemaessBB",
    "StruktureinheitBebaubar": "Struktureinheit",
}

GOLD_PREFIX = "GOLD"
GOLD_COLOR = "FFD700"
GRAY_COLOR = "DCDCDC"

ROW_HEIGHT = 75

ANNOTATOR_NAME_INDEX = -4
DO_NOT_ANNOTATE = "DON'T ANNOTATE THIS SENTENCE"


class Review:
    OK = "OK"
    MISSING = "MISSING"
    ERROR = "ERROR"


class DocumentFields:
    ID = "id"
    SENS = "sens"
    ANNOTATORS = "annotators"
    FULL_ANNOTATORS = "full_annotators"
    LABELS_GOLD = "labels_gold"
    FULL_GOLD = "full_gold"
    LABELS_REVIEWERS = "labels_reviewers"
    FULL_REVIEWERS = "full_reviewers"


class SenFields:
    ID = "id"
    TEXT = "text"
    GOLD_MODALITY = "gold_modality"
    ALREADY_GOLD_ON_ANNOTATION = "already_gold_on_annotation"
    GEN_ATTRIBUTES_ON_ANNOTATION = "gen_attributes_on_annotation"
    GEN_ATTRIBUTES_ON_FULL_ANNOTATION = "gen_attributes_on_full_annotation"
    GEN_ATTRIBUTES = "gen_attributes"
    LABELS_GOLD_EXISTS = "labels_gold_exists"
    FULL_GOLD_EXISTS = "full_gold_exists"
    GOLD_ATTRIBUTES = "gold_attributes"
    ANNOTATED_ATTRIBUTES = "annotated_attributes"
    FULL_ANNOTATED_ATTRIBUTES = "full_annotated_attributes"
    ATTRIBUTES = "attributes"
    SEGMENTATION_ERROR = "segmentation_error"


class AttributeFields:
    NAME = "name"
    TYPE = "type"
    VALUE = "value"


class AnnotatedAttributeFields:
    ANNOTATORS = "annotators"


class FullAnnotatedAttributeFields:
    ATTRIBUTES = "attributes"
    MODALITY = "modality"


class OldDocumentFields:
    ID = "id"
    SECTIONS = "sections"


class OldSectionFields:
    SENS = "sens"


class OldSenFields:
    ID = "sen_id"
    TEXT = "text"
    GEN_ATTRIBUTES = "gen_attributes"
    ATTRIBUTES = "attributes"


class AttributesNames:
    AbschlussDachMaxBezugGebaeude = "AbschlussDachMaxBezugGebaeude"
    AnFluchtlinie = "AnFluchtlinie"
    AnordnungGaertnerischeAusgestaltung = "AnordnungGaertnerischeAusgestaltung"
    AusnahmeGaertnerischAuszugestaltende = "AusnahmeGaertnerischAuszugestaltende"
    BegruenungDach = "BegruenungDach"
    DachneigungMax = "DachneigungMax"
    Dachart = "Dachart"
    DurchgangBreite = "DurchgangBreite"
    DurchgangHoehe = "DurchgangHoehe"
    ErrichtungGebaeude = "ErrichtungGebaeude"
    Flaechen = "Flaechen"
    GebaeudeBautyp = "GebaeudeBautyp"
    GebaeudeHoeheArt = "GebaeudeHoeheArt"
    GebaeudeHoeheMax = "GebaeudeHoeheMax"
    GehsteigbreiteMin = "GehsteigbreiteMin"
    PlangebietAllgemein = "PlangebietAllgemein"
    Planzeichen = "Planzeichen"
    StrassenbreiteMin = "StrassenbreiteMin"
    VerkehrsflaecheID = "VerkehrsflaecheID"
    VonBebauungFreizuhalten = "VonBebauungFreizuhalten"
    VorkehrungBepflanzung = "VorkehrungBepflanzung"
    WidmungInMehrerenEbenen = "WidmungInMehrerenEbenen"
    WidmungUndZweckbestimmung = "WidmungUndZweckbestimmung"


class AttributeTypes:
    CONDITION = "condition"
    CONTENT = "content"
    CONDITION_EXCEPTION = "conditionException"
    CONTENT_EXCEPTION = "contentException"


class Modalities:
    OBLIGATION = "obligation"
    PERMISSION = "permission"
    PROHIBITION = "prohibition"


EMPTY = "EMPTY"
