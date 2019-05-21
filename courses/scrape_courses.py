import requests
from bs4 import BeautifulSoup, Tag, NavigableString
from urllib.parse import urljoin


def scrape_mccormick_courses(dept="computer-science"):
    # download the index page
    index_url = "https://www.mccormick.northwestern.edu/"+dept+"/courses/"
    index_page = requests.get(index_url)
    # load the page into beautifulsoup for parsing
    index = BeautifulSoup(index_page.content, 'html.parser')

    # get the rows in the course table
    rows = index.select('#course_list tr')
    for i, row in enumerate(rows):
        # skip the first row of table headers
        if i == 0:
            continue

        # use CSS selectors to search just within this row
        number = row.select_one('td:nth-of-type(1)').text
        title = row.select_one('td:nth-of-type(2)').text
        anchor_element = row.select_one('a')
        # get the "href" attribute from the "a" element we found above
        relative_url = anchor_element['href']
        absolute_url = urljoin(index_url, relative_url)

        print(number, title, absolute_url)

        # now download the course detail page
        detail = BeautifulSoup(requests.get(absolute_url).content, 'html.parser')

        # parse prereqs and description
        prereqs = None
        description = None
        for h3 in detail.select("#main-content h3"):
            if h3.next_sibling:
                s = h3.next_sibling
                text_after_h3 = s.get_text() if isinstance(s, Tag) else s

                if h3.text == "Prerequisites":
                    prereqs = text_after_h3
                if h3.text == "Description":
                    description = text_after_h3
        print("Prereqs:", prereqs)
        print("Description:", description, "\n")


if __name__ == '__main__':
    scrape_mccormick_courses("computer-science");
    scrape_mccormick_courses("industrial");

