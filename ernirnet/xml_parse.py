from xml.dom.minidom import parseString
import urllib2


class Parser:

    def get_mw_data(self, id):

        abilities = self.parse_mw_sheet(id)

        data = dict(status=200)
        data["message"] = "OK"
        data["content"] = dict(abilityScores = abilities)

        return data

    def parse_mw_sheet(self, id):
        xml_path = "http://www.myth-weavers.com/sheetview.php?sheetid=" + str(id)

        xml_response = urllib2.urlopen(xml_path)  # TODO: Error handling. Right.
        xml_string = xml_response.read()

        # Stripping away all XML not between the first instance of the defined strings (inclusive)
        new_xml_string = self.get_valid_block(xml_string, '<table id="statblock">', '</table>')

        dom = parseString(new_xml_string)

        ability_scores = []
        # Extracting the values corresponding to the six ability scores
        for sub_element in dom.getElementsByTagName("input"):
            if sub_element.hasAttribute("class"):
                if sub_element.attributes["class"].value == "mod" and "Mod" in sub_element.attributes["name"].value:
                    ability_scores.append(int(sub_element.attributes["value"].value))

        return ability_scores

    def get_valid_block(self, xml, start_string, end_string):
        # So, why am I extracting a sub-block rather than relying on the DOM parser?
        # MW documents are not all well formed XML, it seems.
        lines = xml.split("\n")

        new_xml_string = ""
        appending = False
        for line in lines:
            line = line.lstrip()
            if not appending:
                if start_string in line:
                    appending = True
            if appending:
                new_xml_string += line

            if appending and end_string in line:
                break
        return new_xml_string

    def __init__(self):
        pass