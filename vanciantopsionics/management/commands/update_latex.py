from django.core.management.base import BaseCommand
from vanciantopsionics.models import Chapter, Section, Subsection, \
    Subsubsection
from bs4 import BeautifulSoup
from django.utils.text import slugify
import os
import sys
import re
import subprocess
import time


class Command(BaseCommand):

    @classmethod
    def walk_tex_tree(cls, base_folder, base_filepath):
        """
        Takes a .tex files, and parses its \include commands to make one
        big happy document.

        :param base_folder: A path to a folder containing .tex files.
        :param base_filepath: A path to a file that may or may not have
        \include commands.
        :return: A concatenated file.
        """
        base_file = cls.read_file_to_list(base_filepath)

        input_pattern = re.compile(r"\\input\{(?P<rel_path>.*)\}")
        output_file = []

        lineno = 0
        for line in base_file:
            input_match = re.match(input_pattern, line)
            if input_match:
                new_filepath = base_folder + input_match.group("rel_path")
                addition = cls.walk_tex_tree(base_folder, new_filepath)
                lineno += len(addition)
                output_file = \
                    output_file[:lineno] \
                    + addition \
                    + base_file[lineno:]
            else:
                output_file.append(line)
            lineno += 1

        return output_file

    @classmethod
    def get_chapter_names(cls, base_path):
        """

        :param base_path: A path to a folder containing .tex files.
        :return: A list of all .tex filepaths in the base folder and its
        subdirectories that have "Chapter" in the file name.
        """
        tex_file_names = []

        for (path, directories, files) in os.walk(base_path):
            for filename in files:
                if re.match(r"_Chapter.*\.tex$", filename):
                    full_name = os.path.join(path, filename)
                    tex_file_names.append(full_name)

        return sorted(tex_file_names)

    @classmethod
    def read_file_to_list(cls, file_path):
        """

        :param file_path: A path to a .tex document.
        :return: A list containing each line of the document on own line.
        """
        file = open(file_path, "r")
        return [line for line in file]

    @classmethod
    def preprocess_file(cls, current_batch, links):
        """
        Preprocesses a list of strings so that Pandoc can handle them.

        :param current_batch: A list of strings, each representing a line
        of LaTeX code.
        :return: A list of strings, cleaned up for Pandoc.
        """

        # Links
        link_pattern = r"(?P<whole_link>\\nameref\{(?P<label>.*?)\})"

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

        # Section headings
        # ToDo use the longnames instead?
        section_pattern = re.compile(r"\\(?P<section_type>chapter|section|subsection|subsubsection|paragraph|subparagraph)(\[(?P<shortname>.*?)\]|\{(?P<longname>.*?)\})")

        lines = []
        special_line_numbers = []
        print_mode = False

        for number, line in enumerate(current_batch):

            # Optional printing for debugging purposes
            if line == "%pandoc_print_begin\n":
                print_mode = True
            if line == "%pandoc_print_end\n":
                print_mode = False

            # Skipping comments
            if line[0] == "%":
                line = ""

            # Handling internal links, turning them into http hyperlinks
            link_matches = re.findall(link_pattern, line)
            for match in link_matches:
                internal_link, label = match
                url = links[label]["url"]
                caption = links[label]["caption"]
                hyperlink = "\href{" + url + "}{" + caption + "}"
                line = line.replace(internal_link, hyperlink)

            # Handling basic tables
            table_match = p_column_pattern.match(line)
            if table_match:
                line = re.sub(r"\|?p\{.*?\}", "l", line)
            rule_match = rule_pattern.match(line)
            if rule_match:
                line = "\hline\n"
            box_match = box_pattern.match(line)
            multicolumn_match = multicolumn_pattern.match(line)
            cmidrule_match = cmidrule_pattern.match(line)
            if box_match or multicolumn_match or cmidrule_match:
                line = ""
            line = line.replace("tableonecolumn", "table")
            line = line.replace("tabular}}}", "tabular}")
            line = line.replace("tabular}}", "tabular}")
            line = line.replace("&Known", "&Spells Known")
            if "tabular" in line:
                special_line_numbers.append(number)

            # Handling enumerated environments
            enumerated_item_match = enumerated_item_pattern.match(line)
            if enumerated_item_match:
                line = "  \item " + "(" + enumerated_item_match.group("number") + \
                       ") " + enumerated_item_match.group("contents")

            # Section headings with short names
            chapter_match = section_pattern.match(line)
            if chapter_match:
                if chapter_match.group("shortname"):
                    line = "\\" \
                           + chapter_match.group("section_type") \
                           + "{" \
                           + chapter_match.group("shortname") \
                           + "}"

            # Other substitutions
            label_match = label_pattern.match(line)
            if label_match:
                line = label_match.group("pre") + label_match.group("post")
            line = line.replace(r"\paragraph", "\n \\textbf")
            line = line.replace(r"\subparagraph", "\n \\emph")

            if print_mode:
                sys.stdout.write(line)

            lines.append(line)

        lines = cls.replace_super_special(lines, special_line_numbers)

        return lines

    @classmethod
    def replace_super_special(cls, lines, line_numbers):
        """
        Some lines are so messed up they must be handled on their own. :(
        """
        for number in line_numbers:
            line = lines[number]

            # Chapter 1
            line = line.replace(r"\begin{tabular}{l*{19}{l}l}", r"\begin{tabular}{lllllllllllllllllllll}")
            line = line.replace(r"\begin{tabular}{l*{9}{c}}", r"\begin{tabular}{llllllllll}")

            lines[number] = line

        return lines


    @classmethod
    def store_chapter(cls, current_batch, current_object):
        """

        :param current_batch: A list of strings, each item representing a
        line of a .tex document.
        :param current_object: A chapter object.
        :return: Nothing, but see parse_section.
        """

        parent_object = None
        current_section_type = "chapter"
        cls.clear_chapter(current_object)

        latest_sec_break = 0
        current_title = current_object.title
        order = current_object.order

        for line_no, line in enumerate(current_batch):

            section_match = re.match(r"\\(?P<section_type>section|subsection|subsubsection)\{(?P<title>.*?)\}", line)
            if section_match:

                # Start by flushing in all the data we've read so far for
                # this particular section
                lines = current_batch[latest_sec_break+1:line_no]
                cls.parse_section(current_title, lines, order, current_object, parent_object)

                # And then massive branching to see where the next section
                # belongs in the document tree. :(
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

                current_title = section_match.group("title")
                latest_sec_break = line_no

        lines = current_batch[latest_sec_break+1:]
        cls.parse_section(current_title, lines, order, current_object, parent_object)

    @classmethod
    def parse_section(cls, title, input_lines, order, current_object, parent):
        """
        Takes in .tex info, stores equivalent .html info in the given
        model instance.

        :param title: The title of the current lexical section to store.
        :param input_lines: A list of the lines the current section should
        have, in .tex format.
        :param order: The order of the current section, relative to
        sections of the same level.
        :param current_object: The actual chapter, section, subsection
         or subsubsection instance.
        :param parent: A reference to the section's parent in the
        document structure
        :return: The modified section object.
        """
        if parent: # Chapters don't need more work.
            tex_base = "".join(input_lines)
            html_source = cls.call_pandoc(tex_base)

            current_object.title = title
            current_object.first_text = html_source
            current_object.order = order
            current_object.parent = parent

            current_object.save()
        return current_object

    @classmethod
    def clear_chapter(cls, chapter_object):
        """
        Deletes all lexical children of the given chapter object instance.
        """
        for section in chapter_object.section_set.all():
            section.delete()

    @classmethod
    def postprocess_chapter(cls, chapter, link_dict):
        """
        Applies postprocess_text to all lexical children of the given
        chapter.

        :param chapter: A Chapter model instance.
        :param link_dict: A dictionary object as given by
        generate_link_dict.
        :return: None
        """
        clean = cls.postprocess_text(chapter.first_text, link_dict)
        chapter.first_text = clean
        chapter.save()
        for s in chapter.section_set.all():
            clean = cls.postprocess_text(s.first_text, link_dict)
            s.first_text = clean
            s.save()
            for ss in s.subsection_set.all():
                clean = cls.postprocess_text(ss.first_text, link_dict)
                ss.first_text = clean
                ss.save()
                for sss in ss.subsubsection_set.all():
                    clean = cls.postprocess_text(sss.first_text, link_dict)
                    sss.first_text = clean
                    sss.save()


    @classmethod
    def postprocess_text(cls, input_string, link_dict):
        """
        Cleans up some HTML artifacts left by Pandoc.

        :param input_string: A string of html code, as returned by Pandoc.
        :param link_dict: A dictionary object as given by
        generate_link_dict.
        :return: A cleaner, slightly less invalid html string.
        """
        soup = BeautifulSoup(input_string, "html.parser")

        # Fixing table classes
        for table in soup.find_all("table"):
            table["class"] = "table"

        # Fixing table labels
        old_labels = soup.find_all(text=re.compile("\[tab:"))
        for old_label in old_labels:
            for sibling in old_label.parent.next_siblings:
                if sibling.name == "table":
                    label_name = old_label[1:-1]
                    new_id = slugify(label_name[4:])
                    sibling["id"] = new_id
                    old_label.parent.extract()

                    if label_name in link_dict:
                        new_tag = soup.new_tag("caption")
                        new_tag.string = "Table: " + link_dict[label_name]["caption"]
                        sibling.insert(0, new_tag)

                    break

        return str(soup)

    @classmethod
    def generate_link_dict(cls, d, current_batch, chapter_number):
        """

        :param d: A dictionary, containing latex labels as keys. As values,
        there are tuples the label's new url-to be and the corresponding
        caption.
        :param current_batch: A list of strings where each item in the list
        is one line of a .tex document.
        :param chapter_number: The number of the current chapter.
        :return:
        """
        for line in current_batch:

            chapter_match = re.match(
                r"\\(?P<section_type>chapter|section|subsection|subsubsection|paragraph|subparagraph)(\[(?P<shortname>.*?)\]|\{(?P<longname>.*?)\})",
                line)
            if chapter_match:
                if chapter_match.group("shortname"):
                    name = chapter_match.group("shortname")
                else:
                    name = chapter_match.group("longname")

            caption_match = re.match(r"\\caption\{(.*)\}", line)
            if caption_match:
                # If the caption comes after the label, all is okay,
                # This should not be an issue in recent document versions.
                name = caption_match.group(1)

            label_match = re.match(r"\\label\{(.*)\}", line)
            if label_match:
                label = label_match.group(1)

                # Spells and feats have special rules
                if label[0:4] == "Feat":
                    # Some feat names have additional
                    # square brackets in the title
                    extra_tags = re.match(r"(.*)]", name)
                    if extra_tags:
                        name = extra_tags.group(1)

                d[label] = {
                    "url": "/vanciantopsionics/chapter/"
                           + str(chapter_number)
                           + "/#"
                           + slugify(name), #ToDo use the tocify.js pretty hashing function instead.
                    "caption": name
                }

        return d

    @classmethod
    def parse_main(cls):
        base_folder = "./vanciantopsionics/latex/"
        base_filepath = base_folder + "VancianToPsionics.tex"
        lines = cls.read_file_to_list(base_filepath)

        # RegExes for matching all sorts of things in the main file
        chapter_title_pattern = re.compile(r"\\part\{(?P<title>.*?)\}")
        input_begin_pattern = re.compile(r"\\input\{(?P<path>.*?)\}")

        chapters = {}

        for line_no, line in enumerate(lines):
            chapter_begin_match = chapter_title_pattern.match(line)
            if chapter_begin_match:
                latest_sec_break = line_no+1
                current_title = chapter_begin_match.group("title")

            input_begin_match = input_begin_pattern.match(line)
            if input_begin_match:
                path = input_begin_match.group("path")
                if not "Other" in path:
                    # Then we're done parsing the chapter's initial text
                    tex_text = "".join(lines[latest_sec_break:line_no])
                    html_text = cls.call_pandoc(tex_text)
                    chapter = {
                        "title": current_title,
                        "first_text": html_text
                    }
                    chapters[(base_folder + path)] = chapter
        return chapters


    @classmethod
    def call_pandoc(cls, input_string):
        """

        :param input_string: a string containing a .tex document.
        :return: the result of piping input_string to
        pandoc -f latex -t html
        """

        process = subprocess.Popen(["pandoc -f latex -t html"],
                                   stdin=subprocess.PIPE, shell=True,
                                   stdout=subprocess.PIPE)
        out, err = process.communicate(bytes(input_string, "UTF-8"))

        return out.decode("UTF-8")

    def handle(self, *args, **options):
        start = time.clock()
        base_folder = "./vanciantopsionics/latex/"
        chapter_filenames = self.get_chapter_names(base_folder)

        # ToDo: actually dig this information out of the file...
        chapter_name_dict = self.parse_main()

        link_dict = {}

        #ToDo: Remove horrible duplication
        order = 1
        for file_name in chapter_filenames:
            batch = self.walk_tex_tree(base_folder, file_name)
            link_dict = self.generate_link_dict(link_dict, batch, order)
            order += 1
        dprint("Link index compiled.")

        for chapter in Chapter.objects.all():
            chapter.delete()

        order = 1
        for file_name in chapter_filenames:
            start_chapter_parse = time.clock()
            batch = self.walk_tex_tree(base_folder, file_name)
            batch = self.preprocess_file(batch, link_dict)
            chapter = Chapter()
            chapter.title = chapter_name_dict[file_name]["title"]
            chapter.first_text = chapter_name_dict[file_name]["first_text"]
            chapter.filepath = file_name
            chapter.order = order
            chapter.save()

            self.store_chapter(batch, chapter)
            self.postprocess_chapter(chapter, link_dict)

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