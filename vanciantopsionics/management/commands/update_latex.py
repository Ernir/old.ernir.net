from django.core.management.base import BaseCommand
from vanciantopsionics.models import Chapter
from vanciantopsionics.utils import FileManagement, PostProcessing, PandocManager, PreProcessing
import time


class Command(BaseCommand):

    def handle(self, *args, **options):
        start = time.clock()
        base_folder = "./vanciantopsionics/latex/"
        chapter_filenames = FileManagement.get_chapter_names(base_folder)

        chapter_name_dict = FileManagement.parse_main()

        link_dict = {}

        #ToDo: Remove horrible duplication
        order = 1
        for file_name in chapter_filenames:
            batch = FileManagement.walk_tex_tree(base_folder, file_name)
            link_dict = PreProcessing.generate_link_dict(link_dict, batch, order)
            order += 1
        dprint("Link index compiled.")

        for chapter in Chapter.objects.all():
            chapter.delete()

        order = 1
        for file_name in chapter_filenames:
            start_chapter_parse = time.clock()
            batch = FileManagement.walk_tex_tree(base_folder, file_name)
            batch = PreProcessing.preprocess_file(batch, link_dict)
            chapter = Chapter()
            chapter.title = chapter_name_dict[file_name]["title"]
            chapter.first_text = chapter_name_dict[file_name]["first_text"]
            chapter.filepath = file_name
            chapter.order = order
            chapter.save()

            PandocManager.store_chapter(batch, chapter)
            PostProcessing.postprocess_chapter(chapter, link_dict)

            time_elapsed = time.clock() - start_chapter_parse
            dprint("Chapter " + str(order) + " compiled in " + str(time_elapsed) + "s.")
            order += 1

        time_elapsed = time.clock() - start
        dprint("Compilation finished in " + str(time_elapsed) + "s.")


def pprint(input_object):
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(input_object)


debug = False


def dprint(input_object):
    if debug:
        print(input_object)