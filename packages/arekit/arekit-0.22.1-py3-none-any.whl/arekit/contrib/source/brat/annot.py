from arekit.contrib.source.brat.entities.entity import BratEntity
from arekit.contrib.source.brat.relation import BratRelation


class BratAnnotationParser:

    ENTITIES = "entities"
    RELATIONS = "relations"

    @staticmethod
    def __non_prefixed_id(value):
        assert (isinstance(value, str))
        return value[1:]

    @staticmethod
    def handle_entity(args):

        if not str.isdigit(args[2]) or not str.isdigit(args[3]):
            return None

        e_id = int(BratAnnotationParser.__non_prefixed_id(args[0]))
        e_str_type = args[1]
        e_begin = int(args[2])
        e_end = int(args[3])
        e_value = " ".join([arg.strip().replace(',', '') for arg in args[4:]])

        return BratEntity(id_in_doc=e_id,
                          e_type=e_str_type,
                          index_begin=e_begin,
                          index_end=e_end,
                          value=e_value)

    @staticmethod
    def handle_relation(args):

        e_id = args[0][1:]

        rel_type = args[1]
        source_id = args[2].split(':')[1]
        target_id = args[3].split(':')[1]

        return BratRelation(id_in_doc=e_id,
                            source_id=int(BratAnnotationParser.__non_prefixed_id(source_id)),
                            target_id=int(BratAnnotationParser.__non_prefixed_id(target_id)),
                            rel_type=rel_type)

    @staticmethod
    def parse_annotations(input_file, encoding='utf-8'):
        """ Read annotation collection from file
        """
        entities = []
        relations = []

        for line in input_file.readlines():
            line = line.decode(encoding)

            args = line.split()

            record_type = args[0][0]

            # Entities (objects) are prefixed with `T`
            if record_type == "T":
                entity = BratAnnotationParser.handle_entity(args)
                if entity is not None:
                    entities.append(entity)

            elif record_type == "R":
                relations.append(BratAnnotationParser.handle_relation(args))

        return {
            BratAnnotationParser.ENTITIES: entities,
            BratAnnotationParser.RELATIONS: relations
        }
