import re
from django.core.management.base import BaseCommand
from vanciantopsionics.models import Chapter, Spell, CharacterClass
from vanciantopsionics.utils import (
    FileManagement,
    PreProcessing,
    PandocManager,
    PostProcessing,
)
import time


class Command(BaseCommand):
    def handle(self, *args, **options):
        # ToDo split this into more functions.
        start = time.clock()
        base_folder = "./vanciantopsionics/latex/"
        chapter_filenames = FileManagement.get_chapter_names(base_folder)
        chapter_filenames = natural_sort(chapter_filenames)
        spell_files = [
            base_folder + "Chapter6Spells/Spells.tex",
            base_folder + "Chapter9New/Spells.tex",
        ]
        class_files = [
            base_folder + "Chapter3Classes/Classes.tex",
            base_folder + "Chapter9New/Classes.tex",
        ]

        chapter_name_dict = FileManagement.parse_main()
        link_dict = {}

        # First: Generate the link dictionary.
        order = 1
        for file_name in chapter_filenames:
            batch = FileManagement.walk_tex_tree(base_folder, file_name)
            link_dict = PreProcessing.generate_link_dict(link_dict, batch, order)
            order += 1
        for file_name in spell_files:
            batch = FileManagement.read_file_to_list(file_name)
            link_dict = PreProcessing.generate_link_dict(link_dict, batch)
        for file_name in class_files:
            batch = FileManagement.walk_tex_tree(base_folder, file_name, False)
            link_dict = PreProcessing.generate_link_dict(link_dict, batch)
        dprint("Link index compiled in " + str(time.clock() - start) + "s.")

        for chapter in Chapter.objects.all():
            chapter.delete()

        # Second: Make chapters.
        order = 1
        for file_name in chapter_filenames:
            start_time = time.clock()
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

            time_elapsed = time.clock() - start_time
            dprint("Chapter " + str(order) + " compiled in " + str(time_elapsed) + "s.")
            order += 1

        # The classes are a special case
        start_time = time.clock()
        CharacterClass.objects.all().delete()
        for file_name in class_files:
            for (
                class_filename,
                class_type,
                non_core,
            ) in FileManagement.extract_class_paths(file_name):
                batch = FileManagement.read_file_to_list(base_folder + class_filename)
                PandocManager.store_class(batch, link_dict, class_type, non_core)
        time_elapsed = time.clock() - start_time
        dprint("Classes parsed in " + str(time_elapsed) + "s.")

        # The spell list is as well
        start_time = time.clock()
        Spell.objects.all().delete()
        for file_name in spell_files:
            batch = FileManagement.read_file_to_list(file_name)
            if "New" in file_name:
                non_core = True
            else:
                non_core = False
            PandocManager.process_spell_page(batch, link_dict, non_core)
        time_elapsed = time.clock() - start_time
        dprint("Spells parsed in " + str(time_elapsed) + "s.")

        time_elapsed = time.clock() - start
        dprint("Compilation finished in " + str(time_elapsed) + "s.")


def pprint(input_object):
    import pprint

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(input_object)


debug = True


def dprint(input_object):
    if debug:
        print(input_object)


def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split("([0-9]+)", key)]
    return sorted(l, key=alphanum_key)
