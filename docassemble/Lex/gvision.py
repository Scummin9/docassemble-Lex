# Trial Legend ©2021 Scott Cumming - ALL RIGHTS RESEVERED
from docassemble.base.util import (
    get_config,
    DAList,
    path_and_mimetype,
    DAOAuth,
    DAWeb,
    DAWebError,
    DAObject,
    log,
    Thing,
    format_date,
    format_time,
    date_difference,
    date_interval,
    current_datetime,
    DAFile,
    DAFileList,
    url_ask,
    pdf_concatenate,
)
from docassemble.base.functions import word, single_paragraph, ensure_definition
import numpy as np
from typing import Tuple, Union
import cv2
import re
import math
from .cases36 import possessify

        
__all__ = ["contour_this","contour_margin", "otsu", "inverted_otsu", "remove_horizontal_lines", "remove_vertical_lines", "remove_white_margins", "confuto_terminum", "quaero_rrfps", "normalize_filled", "match_normalized", "ucji_getter", "replace_newlines", "replace_underscores", "case_name_italicizer", "italics", "space_ucji", "len_lines", "get_madlibs"]

def get_madlibs(text):
  madlibs = []
  madlibRegex = re.compile(r"""\[(.+?)\]""", re.DOTALL)
  madlibs_found = madlibRegex.findall(text)
  for madlib in madlibs_found:
    madlibs.append(madlib)
  return madlibs
      
def italics(text, default=None):
    """Adds Markdown tags to make the text bold if it is not blank."""
    ensure_definition(text, default)
    if text is None or text == '':
        if default is None:
            return ''
        return '*' + str(default) + '*'
    return '*' + re.sub(r'\*', '', str(text)) + '*'

def case_name_italicizer(text):
  
  casenameRegex = re.compile(r"""((\n|\A|\. |; |\a)(((See, e\.g\.)(,\s))?([A-Za-z,\s&-]+(\sv\.\s)[A-Za-z,\s\.&-]+))(, \d{1,3} (Or )(App )?)((at \d{1,3})|((.+?)\(\d{4}\))))""", re.DOTALL)
  text2 = str(re.sub(casenameRegex, r'\g<2>*\g<3>*\g<9>\g<12>', text))
  
  signalRegex = re.compile(r"""(\n|\A|\. |; |\a|\: )(((((B|b)ut\s)?((S|s)ee)?(,)?\s((((e|E)\.g\.)(,))|(generally)|(also))))(\s[ORSECUJI]{3,4}))""", re.DOTALL)
  text3 = str(re.sub(signalRegex, r'\g<1>*\g<3>*\g<17>', text2))
  
  return text3

def len_lines(text):
  paras_regex = re.compile(r"""[\a\n]+""")
  paras = re.split(paras_regex, text)
  total_lines = 0
  for para in paras:
    para_lines = int(math.floor(len(para) / 100))

    total_lines += para_lines + 2
  return total_lines + 2

        
def space_ucji(jury_instruction, index):
    # 48 lines for the first page, 52 lines for the rest
    text = jury_instruction.instruction
    paras_regex = re.compile(r"""[\a\n]+""")
    paras = re.split(paras_regex, text)
    if len(jury_instruction.comment):
        comment = str(jury_instruction.comment_title + " " + jury_instruction.comment)
        comment_lines = len_lines(comment)
    else:
        comment_lines=0
        comment=""
    lines_per_page = [48] + [52] * (len(text) // 260 + 1)
    index_string = possessify("Plaintiff", "Requested Jury Instruction ") + str(index + 1)
    if "Special Instruction" in jury_instruction.no:
        number_string = str(jury_instruction.no)
    else:
        number_string = str("UCJI No. " + jury_instruction.no)

    pages = []
    current_page = ''
    current_page_lines = 0
    the_page = 1
    for para in paras:

        # add 2 lines for paragraph separator
        if current_page_lines + 5 > lines_per_page[0]:
            # add new page
            pages.append(current_page + '\a' * (lines_per_page[0] - current_page_lines - 4) + index_string + "-" + str(
                int(the_page)) + "\a" + number_string + "\a")
            current_page = ''
            current_page_lines = 0
            lines_per_page.pop(0)
            the_page += 1
        # calculate number of lines for current paragraph
        para_lines = int(math.floor(len(para) / 100))
        #if para_lines == 0:
        #    para_lines += 1
        # check if adding the paragraph will exceed the maximum lines for the page
        if current_page_lines + para_lines + 6 > lines_per_page[0]:
            # add new page
            pages.append(current_page + '\a' * (lines_per_page[0] - current_page_lines - 4) + index_string + "-" + str(
                int(the_page)) + "\a" + number_string + "\a")
            current_page = ''
            current_page_lines = 0
            lines_per_page.pop(0)
            the_page += 1
        # add paragraph to current page
        current_page += para + '\a\a'
        current_page_lines += para_lines + 2

    # add remaining text to last page
    if current_page:
        if len(pages):
            pages.append(current_page + '\a' * (lines_per_page[0] - current_page_lines - comment_lines - 4))
            comment_matter = str(str(jury_instruction.comment + "\a\a") if len(jury_instruction.comment ) else "")  + "\a"+ index_string + "-" + str( int(the_page)) + "\a" + number_string
        else:
            pages.append(current_page + '\a' * (lines_per_page[0] - current_page_lines - comment_lines - 4)) 
            comment_matter = str(str(jury_instruction.comment + "\a\a") if len(jury_instruction.comment ) else "")  + "\a"+ index_string + "\a" + number_string

    return (pages, jury_instruction.comment_title, comment_matter)
  


def replace_underscores(text):
    underscoreRegex = re.compile(r"_")
    text2 = str(underscoreRegex.sub("", text))
    return text2

def replace_newlines(text):
    newlineRegex = re.compile(r"\n")
    text2 = str(newlineRegex.sub("\a", text))
    return text2
  
def ucji_getter(text):
    instructions = []
    ucjiRegex = re.compile(r"""((UCJI\s((\d){1,2}\.(\d){1,2}[A-Z]?)\s([A-Z]+(.+?)))(Download MS Word)(.+?)((COMMENT: |CAVEAT: )(.+?))?((\d{1,2})(\/)(\d{1,2})))""", re.DOTALL)
    
    #[1] "UCJI 10.05 PHYSICAL FACTS"
    ##[2] "10.05"
    ###[5] "PHYSICAL FACTS"
    
    #[8] "Your factual conclusions cannot be based on evidence that is contrary to established physical [fact..."
    ##[10] "COMMENT: "
    ###[11] "See generally Marshall v. Martinson, 268 Or 46, 58, 518 P2d 1312 (1974); Sturm v. Smelcer, 235 Or 25..."
    
    #[12] "12/13"
    ##[13] "12"
    ###[15] "13"
    #newlineRegex = re.compile(r"\n")
    #text2 = str(newlineRegex.sub(" \a ", text))
    ucjis = ucjiRegex.findall(text)
    for instruction in ucjis:
      
        name = str(instruction[1]).strip()
        no = str(instruction[2]).strip()
        title = str(instruction[5]).strip()
        instr = str(instruction[8]).strip()
        comment_title = str(instruction[10]).strip().lower()
        comment = str(instruction[11]).strip()
        update = str(str(instruction[13]).strip() + "/1/" + str(instruction[15]).strip())
        
        instructions.append((str(name), str(no), str(title), str(instr), str(comment_title), str(comment), str(update)))
        
    return instructions
  
def normalize_filled(thresh):
    try:
      image = thresh.page_path(1, "page")
      img = cv2.imread(image, 0)
    except:
      try: 
        image = thresh[0].page_path(1, "page")
        img = cv2.imread(image, 0)
      except:
        try:
          image = thresh.path()
          img = cv2.imread(image, 0)
        except:
          image = thresh
          img = image
    blur1 = cv2.GaussianBlur(img,(23,23),0)
    _, thresh = cv2.threshold(blur1, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    log("thresh is " + repr(thresh))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 20))
    dilated = cv2.dilate(thresh, kernel, iterations = 8)
    #cnt, _ = cv2.findContours(dilated, 
    #img = otsu(thresh)
    #im = im3.copy()
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cnt, _ = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # fill shape
    #cv2.fillPoly(img, pts=cnt, color=(255,255,255))
    bounding_rect = cv2.boundingRect(cnt[0])
    img_cropped_bounding_rect = img[bounding_rect[1]:bounding_rect[1] + bounding_rect[3], bounding_rect[0]:bounding_rect[0] + bounding_rect[2]]
    # resize all to same size
    img_resized = cv2.resize(img_cropped_bounding_rect, (300, 300))
    alldocfile = DAFile("boxed")
    alldocfile.initialize(filename="boxedfile.png")
    cv2.imwrite(alldocfile.path(), img_resized)
    alldocfile.commit()
    return alldocfile
    return img_resized

def match_normalized(list_of_caption_images, normalized_image_to_compare):
  imgs = list(list_of_caption_images, normalized_image_to_compare)
  imgs = [normalize_filled(i) for i in imgs]
  for i in range(1, 6):
    plt.subplot(2, 3, i), plt.imshow(imgs[i - 1], cmap='gray')
    print(cv2.matchShapes(imgs[0], imgs[i - 1], 1, 0.0))
    
    
# Trial Legend ©2021 Scott Cumming - ALL RIGHTS RESEVERED
def quaero_rrfps(document):
    text = str(document)
    requests = []
    interrogs = []
    admissions = []
    rRFPRegex = re.compile(r"""
          ((\s?\|?\s?\|?\s?((((T|l|I|\|)N(T|l|I|\|)(E|F|L|R)(R|P|L|S|C)(R|P|L|S|C)(O|o|0)GA(T|l|I|\|)(O|o|0)(P|R)Y|Interrogatory)|(((R|P|L|S|C|\<\.|\,|-)?(E|F|L|R)(Q|O)U(E|L|F)S(T|l|I|\|))|Request)\s?((E|L|F)(Q|O)(R|P|L|S|C|\<\.|\,|-)\s(R|P|L|S|C|\<\.|\,|-)(R|P|L|S|C|\<\.|\,|-)(Q|O)DU(R|P|L|S|C)(T|l|I|\|)(T|l|I|\|)(Q|O)N\s)?)?\s?(N(O|o|0)(\.|\,|\:|;)?|NUMBER)\s?)(\_?(\d)+)((\—|\-|\:|\;|\'|\.|\,)))(.+?)(?=(\s?\|?\s?\|?\s?((((T|l|I|\|)N(T|l|I|\|)(E|F|L|R)(R|P|L|S|C)(R|P|L|S|C)(O|o|0)GA(T|l|I|\|)(O|o|0)(P|R)Y|Interrogatory)|(((R|P|L|S|C|\<\.|\,|-)?(E|F|L|R)(Q|O)U(E|L|F)S(T|l|I|\|))|Request)\s?((E|L|F)(Q|O)(R|P|L|S|C|\<\.|\,|-)\s(R|P|L|S|C|\<\.|\,|-)(R|P|L|S|C|\<\.|\,|-)(Q|O)DU(R|P|L|S|C)(T|l|I|\|)(T|l|I|\|)(Q|O)N\s)?)?\s?(N(O|o|0)(\.|\,|\:|;)?|NUMBER)\s?)(\_?(\d)+)((\—|\-|\:|\;|\'|\.|\,)))|(Response)|(Answer)|(ANSW(E|F|L|R)(R|P|L|S|C))|((R|P|L|S|C|\<\.|\,|-)?(E|F|L|R)S(P|R)ONS(E|F|L))|(\s\d?\d\.|Dated|DATED)|\Z))
          """, re.VERBOSE | re.DOTALL)
    ## Group 2 == e.g., "REQUEST NO. 26:" | "4."
    ### Group 36 == e.g., "26" | "4"
    #### Group 40 == " Copies of all correspondence, documents, texts, notes, messages (in any form including electronic) ..."
    OtherRFPRegex = re.compile(
        r"(\s((\_?(\d|I|l|\||i){1,2})((\—|\-|\:|\;|\'|\.)))(.+?)(?=(\s(\_?(\d|I|l|\||i){1,2})((\—|\-|\:|\;|\'|\.|\,)))|(\s\d?\d\.|Dated|DATED)))",
        re.DOTALL,
    )
    casenoRegex = re.compile(
        r"(Case\sNo\.\s\d?\:?(\d\d\-?(CV|cv)\-?\d\d\d\d\d\-?\D?\D?)(?=\n))"
    )
    text2 = str(casenoRegex.sub("", text))
    reqs = rRFPRegex.findall(text2)
    casenotext = casenoRegex.search(text)
    #The following categories are "out of order" so to speak in terms of the integer that identifies them and the occurence of each type. However, if rfps were to come before rfas, the issue arises that "REQUEST NO. X:" is very often used for both discovery requests. Accordingly, if rfas were analyzed after rfps, rfas would occasionally be miscategorized as rfps.
    for req in reqs:
        if (
            "ADMISSION" in req[1].upper()
            or "ADMIT" in req[1].upper()
            or "ADMIT" in req[39].upper()
            or "REQUEST FOR ADMISSION" in req[1].upper()
            or "RFA" in req[1].upper()
        ):
            requests.append((single_paragraph(req[39]).strip(), 2, str(req[35]).strip()))
        elif (
            "INTERROGATORY" in req[1].upper()
            or "INTER" in req[1].upper()
            or "ATORY" in req[1].upper()
            or "ANSWER" in req[1].upper()
            or "ROG" in req[1].upper()
        ):
            requests.append((single_paragraph(req[39]).strip(), 1, str(req[35]).strip()))
        elif (
            "PRODUCTION" in str(req[1]).upper()
            or "PROD" in str(req[1]).upper()
            or "REQUEST" in str(req[1]).upper()
            or "REQ" in str(req[1]).upper()
            or "RESPONSE" in str(req[1]).upper()
            or "RFP" in str(req[1]).upper()
        ):
            requests.append((single_paragraph(req[39]).strip(), 0, str(req[35]).strip()))
        else:
            requests.append((single_paragraph(req[39]).strip(), 3, str(req[35]).strip()))
    if len(requests) < 1:
        requests.clear()
        reqs = OtherRFPRegex.findall(text2)
        for req in reqs:
            requests.append((single_paragraph(req[6]).strip(), 3, str(req[3]).strip()))
            log("The next request is " + repr(single_paragraph(req[6]).strip()))
    requests.append((str(casenotext.group(2)), 0, ""))
    return requests
  
def confuto_terminum(filein, fileout):
    im = cv2.imread(filein, 0)
    imageV = remove_vertical_lines(im, im)
    if imageV[1] == im.shape[:2]:
      log("same shape")
      image2 =  contour_margin(im, im)
    else:
      image2 = imageV[0]
    image3 = remove_horizontal_lines(image2, image2)
    image4 = remove_white_margins(image3)
    blur1 = cv2.GaussianBlur(image4,(3,3),0)
    _, thresh =cv2.threshold(blur1,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT,(1, 1))
    dilated = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel3, iterations=32)
    cv2.imwrite(fileout, dilated)
    return fileout

def remove_horizontal_lines(thresh, fileout):
  try:
      image = thresh.page_path(1, "page")
  except:
      try: 
        image = thresh[0].page_path(1, "page")
      except:
        try:
          image = thresh.path()
        except:
          image = thresh
  try:
      image3 = fileout.page_path(1, "page")
      im3 = cv2.imread(image3, 0)
  except:
      try: 
        image3 = fileout[0].page_path(1, "page")
        im3 = cv2.imread(image3, 0)
      except:
        try:
          image3 = fileout.path()
          im3 = cv2.imread(image3, 0)
        except:
          image3 = fileout
          im3 = image3
  im2 = otsu(thresh)
  im = im3.copy()
  height, width  = im3.shape[:2]
  horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (int(width),1))
  detected_lines = cv2.morphologyEx(im2, cv2.MORPH_OPEN, horizontal_kernel, iterations=3)
  cnts, _ = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  candidates = []
  candidates.clear()
  dice=[]
  log("contours are " + repr(cnts))
  for cnt in cnts:
    leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
    rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
    topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
    bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])
    if topmost[1] !=0:
      dice.append(slice(topmost[1], bottommost[1]))
  log("dice are " + repr(dice))
  for d in dice:
    im3 = np.delete(im3, d, 0)
  return im3

def remove_vertical_lines(thresh, fileout):
  try:
      image = thresh.page_path(1, "page")

  except:
      try: 
        image = thresh[0].page_path(1, "page")
      except:
        try:
          image = thresh.path()
        except:
          image = thresh
  try:
      image3 = fileout.page_path(1, "page")
      im3 = cv2.imread(image3)
  except:
      try: 
        image3 = fileout[0].page_path(1, "page")
        im3 = cv2.imread(image3)
      except:
        try:
          image3 = fileout.path()
          im3 = cv2.imread(image3)
        except:
          im3 = fileout
  im2 = inverted_otsu(thresh)
  vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 15))
  detected_lines = cv2.morphologyEx(im2, cv2.MORPH_OPEN, vertical_kernel, iterations=5)
  cnts, _ = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  candidates = []
  candidates.clear()
  height, width = im3.shape[:2]
  for cnt in cnts:
    leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
    rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
    topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
    bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])
    if bottommost[1]-topmost[1] >= int(height*0.9):
      candidates.append([rightmost[0], [[rightmost[0] , 0], [width+rightmost[0], bottommost[1]]]])
  if len(candidates):
    deminimis=0
    for candidate in candidates:
      if candidate[0]>deminimis:
        deminimis = candidate[0]
        output_specs = candidate[1]
    topleft = output_specs[0]
    bottomright = output_specs[1]
  else:
    topleft = [0,0]
    bottomright = [width, height]
  cropped = im3[topleft[1]:bottomright[1], topleft[0]:bottomright[0]] 
  return [cropped, cropped.shape[:2]]
  alldocfile = DAFile("boxed")
  alldocfile.initialize(filename="boxedfile.png")
  cv2.imwrite(alldocfile.path(), cropped)
  alldocfile.commit()
  return [alldocfile, cropped.shape[:2]]
    
def remove_white_margins(filein):
  try:
      image = filein.page_path(1, "page")
      the_image = cv2.imread(image)
  except:
      try: 
        image = filein[0].page_path(1, "page")
        the_image = cv2.imread(image)
      except:
        try:
          image = filein.path()
          the_image = cv2.imread(image)
        except:
          the_image = filein
  
  original = the_image.copy()
  thresh = inverted_otsu(filein)
  noise_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
  opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, noise_kernel, iterations=2)
  close_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
  close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, close_kernel, iterations=3)
  coords = cv2.findNonZero(close)
  x,y,w,h = cv2.boundingRect(coords)
  cv2.rectangle(the_image, (x, y), (x + w, y + h), (36,255,12), 2)
  crop = original[y:y+h, x:x+w]
  return crop
  alldocfile = DAFile("boxed")
  alldocfile.initialize(filename="boxedfile.png")
  cv2.imwrite(alldocfile.path(), crop)
  alldocfile.commit()
  return alldocfile

def inverted_otsu(filein):
  try:
      image = filein.page_path(1, "page")
      im = cv2.imread(image, 0)
  except:
      try: 
        image = filein[0].page_path(1, "page")
        im = cv2.imread(image, 0)
      except:
        try:
          image = filein.path()
          im = cv2.imread(image, 0)
        except:
          im = filein
  
  blur1 = cv2.GaussianBlur(im,(7,5),0)
  _, thresh =cv2.threshold(blur1, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
  return thresh

def otsu(filein):
  try:
      image = filein.page_path(1, "page")
      log("1")
  except:
      try: 
        image = filein[0].page_path(1, "page")
        log("2")
      except:
        try:
          image = filein.path()
          log("3")
        except:
          image = filein
          log("4")
  try:
    im = cv2.imread(image, 0)
    log("5")
  except:
    im = image
    log("6")
  blur1 = cv2.GaussianBlur(im,(23,23),0)
  _, thresh = cv2.threshold(blur1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
  return thresh
  
def contour_margin(filein, fileout): 
  try:
      image = filein.page_path(1, "page")
      imi = cv2.imread(image, 0)
  except:
      try: 
        image = filein[0].page_path(1, "page")
        imi = cv2.imread(image, 0)
      except:
        try: 
          image = filein.path()
          imi = cv2.imread(image, 0)
        except:
          imi = filein
  try:
      image3 = fileout.page_path(1, "page")
      im3 = cv2.imread(image3, 0)
  except:
      try: 
        image3 = fileout[0].page_path(1, "page")
        im3 = cv2.imread(image3, 0)
      except:
        try:
          image3 = fileout.path()
          im3 = cv2.imread(image3, 0)
        except:
          im3 = fileout
  h, w = imi.shape[:2] 
  im = imi[:int(h*.901), :int(w*.1764705882352941)]
  log("width of the IMI obj is " + repr(w))
  log("height of the IMI obj is " + repr(h))
  rows, columns = im.shape[:2]
  log("width of the IM obj is " + repr(columns))
  log("height of the IM obj is " + repr(rows))
  im2 = im.copy()
  blur1 = cv2.GaussianBlur(im,(23,23),0)
  _, thresh =cv2.threshold(blur1,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
  log("thresh is " + repr(thresh))
  kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 20))
  dilated = cv2.dilate(thresh, kernel, iterations = 8)
  contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  log("contours is " + repr(contours))
  hull = []
  height, width = dilated.shape[:2]
  ht, wdt = im3.shape[:2]
  log("width of the chopped obj is " + repr(width))
  log("width of the OG obj is " + repr(wdt))
  log("height of the chopped obj is " + repr(height))
  log("ht of the OG obj is " + repr(ht))
  candidates = []
  candidates.clear()
  for cnt in contours:
    leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
    rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
    topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
    bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])
    if int(bottommost[1]-topmost[1]) >= int(rows*0.7):
      candidates.append([leftmost[0], [[topmost[1], rightmost[0] ], [bottommost[1], wdt]]])
  log("the candidates are " + repr(candidates))
  if len(candidates):
    deminimis=columns
    for candidate in candidates:
      if candidate[0]<=deminimis:
        deminimis = candidate[0]
        output_specs = candidate[1]
    log("the deminimis is " + repr(deminimis))
    log("the output specs are " + repr(output_specs)) 

    topleft = output_specs[0]
    bottomright = output_specs[1]
    log("topleft[1] is " + repr(topleft[1]) )
    testw = width*.999
    log("width*.999 is " + repr(testw))

    log("the tested deminimis is " + repr(deminimis))
    log("the tested output specs are " + repr(output_specs)) 
  else:
    topleft = (int(ht*.009),0)
    bottomright = (int(ht*.901), wdt)
  cropped = im3[topleft[0]:bottomright[0], topleft[1]:bottomright[1]] 
  return cropped

def contour_this(filein, fileout): 
  try:
      image = filein.page_path(1, "page")
  except:
      try: 
        image = filein[0].page_path(1, "page")
      except:
        try:
          image = filein.path()
        except: 
          image = filein
        
    
  try:
      image2 = fileout.page_path(1, "page")
  except:
      try: 
        image2 = fileout[0].page_path(1, "page")
      except:
        try:
          image2 = fileout.path()
        except:
          image2 = fileout
  im = cv2.imread(image, 0)
  im2 = cv2.imread(image2, 0)
  hit, widt = im.shape[:2]
  hit2, widt2 = im2.shape[:2]
  topleft = [0,0]
  bottomright = [widt, int(hit*.5)]
  topleft2 = [0,0]
  bottomright2 = [widt2, int(hit2*.5)]
  cropp = im[topleft[1]:bottomright[1], topleft[0]:bottomright[0]] 
  cropp2 = im2[topleft2[1]:bottomright2[1], topleft2[0]:bottomright2[0]] 
  imageV = remove_vertical_lines(cropp, cropp)
  if imageV[1] == cropp.shape[:2]:
    log("same shape")
    image2 =  contour_margin(cropp, cropp)
  else:
    image2 = imageV[0]
  #image3 = remove_horizontal_lines(image2, image2)
  image4 = remove_white_margins(image2)
    
  imageC = remove_vertical_lines(cropp2, cropp2)
  if imageC[1] == cropp2.shape[:2]:
    log("same shape")
    
    image5 =  contour_margin(cropp2, cropp2)
  else:
    image5 = imageC[0]
  #image6 = remove_horizontal_lines(image5, image5)
  image7 = remove_white_margins(image5)
  gauss = (7, 5)
  rect = (6, 17)
  #rect = (3, 80)
  itera = 5
  
  
  blur1 = cv2.GaussianBlur(image4, gauss, 0)
  _, thresh =cv2.threshold(blur1,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
  log("thresh is " + repr(thresh))
  kernel = cv2.getStructuringElement(cv2.MORPH_RECT, rect)
  
  
  dilated = cv2.dilate(thresh, kernel, iterations = itera)
  dilated_alldocfile = DAFile("dilated_boxed")
  dilated_alldocfile.initialize(filename="dilated_boxedfile.png")
  cv2.imwrite(dilated_alldocfile.path(), dilated)
  dilated_alldocfile.commit()
  
  blur2 = cv2.GaussianBlur(image7, gauss, 0)
  _, thresh2 =cv2.threshold(blur2,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
  log("thresh is " + repr(thresh))
  kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, rect)
  
  
  dilated2 = cv2.dilate(thresh2, kernel2, iterations = itera)
  dilated_alldocfile2 = DAFile("dilated_boxed2")
  dilated_alldocfile2.initialize(filename="dilated_boxedfile2.png")
  cv2.imwrite(dilated_alldocfile2.path(), dilated2)
  dilated_alldocfile2.commit()
  
  
  retval =cv2.matchShapes(dilated, dilated2, cv2.CONTOURS_MATCH_I1, 0)
  retval2 =cv2.matchShapes(dilated, dilated2, cv2.CONTOURS_MATCH_I2, 0)
  retval3 =cv2.matchShapes(dilated, dilated2, cv2.CONTOURS_MATCH_I3, 0)
  return [retval, dilated_alldocfile, dilated_alldocfile2, retval2, retval3, repr(gauss), repr(rect), str(itera)]


  contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  log("contours is " + repr(contours))
  hull = []
  blur = cv2.GaussianBlur(im2,(5,5),0)
  _, th3 =cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
  kernel3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3, 3))
  opening = cv2.morphologyEx(th3, cv2.MORPH_OPEN, kernel3)
  cv2.drawContours(opening, contours[2:-1], -1, (0, 0, 0), 10)
  alldocfile = DAFile("boxed")
  alldocfile.initialize(filename="boxedfile.png")
  cv2.imwrite(alldocfile.path(), opening)
  alldocfile.commit()
  return (dilated_alldocfile, alldocfile)
  for contour in contours:
    [x,y,w,h] = cv2.boundingRect(contour)
    cv2.rectangle(im2,(x,y),(x+w,y+h),(255,0,255),2)