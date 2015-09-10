from django.core.management.base import BaseCommand
from vanciantopsionics.models import Chapter, Section, Subsection, Subsubsection
import os
import re
import subprocess


class Command(BaseCommand):

    @classmethod
    def read_file_to_list(cls, file_path):
        file = open(file_path, "r")
        return [line for line in file]

    @classmethod
    def get_tex_names(cls, base_path):
        tex_file_names = []

        # Finds all .tex files in "base_path" as well as all subdirectories
        for (path, directories, files) in os.walk(base_path):
            for filename in files:
                if re.match(r".*\.tex$", filename):
                    full_name = os.path.join(path, filename)
                    tex_file_names.append(full_name)

        return sorted(tex_file_names)

    @classmethod
    def preprocess_file(cls, current_batch):
        """

        :param current_batch: A list of strings, each representing a line
        of LaTeX code.
        :return: A list of strings, cleaned up for Pandoc.
        """
            # Links
        link_pattern = re.compile(
            r"((.*?)(?P<whole_link>\\nameref\{(?P<label>.*?)\})(.*?)*)")

        # Tables
        p_column_pattern = re.compile(r"\\begin\{tabular\}\{(\|?p\{.*?\})+\|?\}")
        rule_pattern = re.compile(r"\\toprule|\\midrule|\\bottomrule")
        box_pattern = re.compile(r"\\makebox\[\\textwidth\]")
        multicolumn_pattern = re.compile(r"(.*)\\multicolumn(.*)")
        cmidrule_pattern = re.compile(r"(.*)\\cmidrule(.*)")

        # Lists
        enumerated_item_pattern = re.compile(r".*\\item\[(?P<number>\d)\](?P<contents>.*)")

        # Labels
        label_pattern = re.compile(r"(?P<pre>.*)\\label\{(Spell|Feat|Sec|sec|Item):(.*)\}(?P<post>.*)")

        lines = []

        for line in current_batch:

            if line[0] == "%":
                continue

            # link_match = link_pattern.match(line)
            # if link_match:
            #     url_components = links[link_match.group("label")]
            #     url = "\href{" + url_components["url"] + "}{" + url_components[
            #         "caption"] + "}"
            #     line = line.replace(link_match.group("whole_link"), url)

            table_match = p_column_pattern.match(line)
            if table_match:
                line = re.sub(r"\|?p\{.*?\}", "l", line)

            rule_match = rule_pattern.match(line)
            if rule_match:
                line = "\hline\n"

            enumerated_item_match = enumerated_item_pattern.match(line)
            if enumerated_item_match:
                line = "  \item " + "(" + enumerated_item_match.group("number") + \
                       ") " + enumerated_item_match.group("contents")

            box_match = box_pattern.match(line)
            multicolumn_match = multicolumn_pattern.match(line)
            cmidrule_match = cmidrule_pattern.match(line)
            if box_match or multicolumn_match or cmidrule_match:
                continue

            label_match = label_pattern.match(line)
            if label_match:
                line = label_match.group("pre") + label_match.group("post")

            line = line.replace("&Known", "&Spells Known")
            line = line.replace("tabular}}}", "tabular}")
            line = line.replace("tabular}}", "tabular}")
            lines.append(line)

        return "".join(current_batch)

    @classmethod
    def store_chapter(cls, current_batch):

        level_map = {
            "chapter": 0,
            "section": 1,
            "subsection": 2,
            "subsubsection": 3
        }

        chapter_name = "Magic Overview"
        current_object = Chapter.objects.get(title=chapter_name)
        order = 1
        parent_object = None
        current_section_type = "chapter"
        cls.clear_chapter(current_object)

        latest_sec_break = 0
        current_title = chapter_name

        for line_no, line in enumerate(current_batch):

            section_match = re.match(r"\\(?P<section_type>section|subsection|subsubsection)(\[(?P<shortname>.*)\]|\{(?P<longname>.*?)\})", line)
            if section_match:

                # Start by flushing in all the data we've read so far for
                # this particular section
                lines = current_batch[latest_sec_break+1:line_no]
                cls.parse_section(current_title, lines, order, current_object, parent_object)

                new_section_type = section_match.group("section_type")
                if new_section_type == "section":
                    if current_section_type == "chapter":
                        order = 1
                        parent_object = current_object
                    elif current_section_type == "section":
                        order += 1  # No change in parent
                    elif current_section_type == "subsection":
                        order = parent_object.order + 1
                        parent_object = parent_object.parent
                    elif current_section_type == "subsubsection":
                        order = parent_object.parent.order + 1
                        parent_object = parent_object.parent.parent
                    current_object = Section()
                elif new_section_type == "subsection":
                    if current_section_type == "section":
                        order = 1
                        parent_object = current_object
                    elif current_section_type == "subsection":
                        order += 1
                    elif current_section_type == "subsubsection":
                        order = parent_object.order + 1
                        parent_object = parent_object.parent
                    current_object = Subsection()
                elif new_section_type == "subsubsection":
                    if current_section_type == "subsection":
                        order = 1
                        parent_object = current_object
                    elif current_section_type == "subsubsection":
                        order += 1
                    current_object = Subsubsection()
                current_section_type = new_section_type

                if section_match.group("shortname"):
                    current_title = section_match.group("shortname")
                else:
                    current_title = section_match.group("longname")
                latest_sec_break = line_no

        lines = current_batch[latest_sec_break+1:]
        cls.parse_section(current_title, lines, order, current_object, parent_object)

    @classmethod
    def parse_section(cls, title, input_lines, order, current_object, parent):
        tex_base = "".join(input_lines)
        html_source = cls.call_pandoc(tex_base)

        current_object.title = title
        current_object.first_text = html_source
        current_object.order = order
        if parent:
            current_object.parent = parent

        current_object.save()
        return current_object

    @classmethod
    def clear_chapter(cls, chapter_object):
        for section in chapter_object.section_set.all():
            section.delete()


    @classmethod
    def call_pandoc(cls, input_string):
        # Pipes the input string to
        #    pandoc -f latex -t html
        # And returns the result.

        process = subprocess.Popen(["pandoc -f latex -t html"],
                                   stdin=subprocess.PIPE, shell=True,
                                   stdout=subprocess.PIPE)
        out, err = process.communicate(bytes(input_string, "UTF-8"))

        return out.decode("UTF-8")

    def handle(self, *args, **options):
        tex_file_names = self.get_tex_names("./vanciantopsionics/latex/Chapter1SpellcastingSystem/")
        batch = self.read_file_to_list(tex_file_names[0])
        self.store_chapter(batch)