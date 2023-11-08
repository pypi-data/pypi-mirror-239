# import os, PyPDF2
# import fitz  # PyMuPDF
#
# def add_filename_as_header(pdf_path, output_path):
#     if not os.path.exists(pdf_path):
#         print("PDF文件不存在：", pdf_path)
#         return
#
#     pdf_document = fitz.open(pdf_path)
#     filename = os.path.basename(pdf_path)
#     filename_no_extension = os.path.splitext(filename)[0]
#
#     for page_num in range(pdf_document.page_count):
#         page = pdf_document[page_num]
#
#         # 添加文件名作为页眉
#         header_text = "PDF文件名：" + filename_no_extension
#         # header_text_bytes = header_text.encode('utf-8')
#         page.insert_text((20, 20), header_text, fontname="chinese_font", fontsize=12)
#
#
#
#     pdf_document.save(output_path)
#     pdf_document.close()
#
# # 批量处理PDF文件
# input_folder = r"C:\Users\Administrator\Desktop\demo\新建文件夹"  # 输入文件夹路径
# output_folder = r"C:\Users\Administrator\Desktop\demo\空文件夹"  # 输出文件夹路径
#
# if not os.path.exists(output_folder):
#     os.makedirs(output_folder)
#
# for filename in os.listdir(input_folder):
#     if filename.endswith(".pdf"):
#         input_pdf_path = os.path.join(input_folder, filename)
#         output_pdf_path = os.path.join(output_folder, filename)
#
#         add_filename_as_header(input_pdf_path, output_pdf_path)
#
# print("已将文件名添加为页眉，并保存到输出文件夹")
# import os, traceback
# import fitz, PyPDF2  #1.26.0  pip install PyPDF2==1.26.0
# import imageio, base64
# import json
# import requests
# from reportlab.pdfgen import canvas  #pip install reportlab
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.pdfbase import pdfmetrics
# from reportlab.lib.pagesizes import A4,landscape
# from reportlab.lib.units import mm
# from frontend import *
# from reportlab.lib.utils import ImageReader

# def add_filename_to_pdf_content(pdf_path, output_path, pic_path):
#     pdfmetrics.registerFont(TTFont('SimHei', 'SimHei.TTF'))
#     for root, dirs, files in os.walk(pdf_path):
#         for file in files:
#             if file.endswith('.pdf'):
#                 src_path = os.path.join(root, file)
#                 des_path = src_path.replace(pdf_path, output_path, 1)
#                 c = canvas.Canvas(des_path)
#                 pdf_name = file.strip('.pdf')
#                 src_pdf_reader = fitz.Document(src_path)
#                 for pg in range(src_pdf_reader.page_count):
#                     page = src_pdf_reader.load_page(pg)  # 获得每一页的对象
#                     trans = fitz.Matrix(3.0, 3.0).prerotate(0)
#                     pm = page.get_pixmap(matrix=trans, alpha=False, dpi=200)
#                     pic_path1 = os.path.join(pic_path, f'{pdf_name}-{str(pg)}.jpg')
#                     pm.save(pic_path1)
#                     c.setPageSize(A4)
#                     c.setFont('SimHei', 12)
#                     c.drawImage(pic_path1, 0 * mm, 0 * mm, 210 * mm, 297 * mm)
#                     c.drawString(10 * mm, 290 * mm, pdf_name)
#                     c.showPage()
#                     os.remove(pic_path1)
#                 c.save()
#
# # 替换为你的PDF文件路径和输出路径
# input_pdf_path = r"C:\Users\Administrator\Desktop\demo\新建文件夹"
# output_pdf_path = r"C:\Users\Administrator\Desktop\demo\保存"
# pic_path = r'C:\Users\Administrator\Desktop\demo\空文件夹'
# try:
#     add_filename_to_pdf_content(input_pdf_path, output_pdf_path, pic_path)
# except Exception as e:
#     print(e)
#     traceback.print_exc()
# def add_filename_to_pdf_content(pdf_path, output_path, pic_path):
#     pdfmetrics.registerFont(TTFont('SimHei', 'SimHei.TTF'))
#     for root, dirs, files in os.walk(pdf_path):
#         for file in files:
#             if file.endswith('.pdf'):
#                 src_path = os.path.join(root, file)
#                 des_path = src_path.replace(pdf_path, output_path, 1)
#                 c = canvas.Canvas(des_path)
#                 pdf_name = file.strip('.pdf')
#                 src_pdf_reader = fitz.Document(src_path)
#                 is_first_page = True  # 标志变量，用于判断是否是第一页
#                 for pg in range(src_pdf_reader.page_count):
#                     page = src_pdf_reader.load_page(pg)  # 获得每一页的对象
#                     trans = fitz.Matrix(3.0, 3.0).prerotate(0)
#                     pm = page.get_pixmap(matrix=trans, alpha=False, dpi=200)
#                     pic_path1 = os.path.join(pic_path, f'{pdf_name}-{str(pg)}.jpg')
#                     pm.save(pic_path1)
#                     c.setPageSize(A4)
#                     c.setFont('SimHei', 12)
#                     c.drawImage(pic_path1, 0 * mm, 0 * mm, 210 * mm, 297 * mm)
#                     if is_first_page:
#                         c.drawString(10 * mm, 290 * mm, pdf_name)
#                         is_first_page = False  # 将标志变量设为False，以确保只在第一页添加文件名
#                     c.showPage()
#                     os.remove(pic_path1)
#                 c.save()
#
# # 替换为你的PDF文件路径和输出路径
# input_pdf_path = r"C:\Users\86130\PycharmProjects\pythonProject1\新建文件夹"
# output_pdf_path = r"C:\Users\86130\PycharmProjects\pythonProject1\保存"
# pic_path = r'C:\Users\86130\PycharmProjects\pythonProject1\空文件夹'
# try:
#     add_filename_to_pdf_content(input_pdf_path, output_pdf_path, pic_path)
# except Exception as e:
#     print(e)
#     traceback.print_exc()


# import os, traceback
# import fitz, PyPDF2
#
# from reportlab.pdfgen import canvas
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.pdfbase import pdfmetrics
# from reportlab.lib.pagesizes import A4,landscape
# from reportlab.lib.units import mm
# import warnings
#
# # 忽略特定类型的警告
# warnings.filterwarnings("ignore")

# def add_filename_to_pdf_content(pdf_path, output_path, pic_path):
#     pdfmetrics.registerFont(TTFont('SimHei', 'SimHei.TTF'))
#     for root, dirs, files in os.walk(pdf_path):
#         for file in files:
#             if file.endswith('.pdf'):
#                 src_path = os.path.join(root, file)
#                 des_path = src_path.replace(pdf_path, output_path, 1)
#                 c = canvas.Canvas(des_path)
#                 pdf_name = file.strip('.pdf')
#                 src_pdf_reader = fitz.Document(src_path)
#                 for pg in range(src_pdf_reader.page_count):
#                     page = src_pdf_reader.load_page(pg)  # 获得每一页的对象
#                     trans = fitz.Matrix(3.0, 3.0).prerotate(0)
#                     pm = page.get_pixmap(matrix=trans, alpha=False, dpi=200)
#                     pic_path1 = os.path.join(pic_path, f'{pdf_name}-{str(pg)}.jpg')
#                     pm.save(pic_path1)
#                     c.setPageSize(A4)
#                     c.setFont('SimHei', 12)
#                     c.drawImage(pic_path1, 0 * mm, 0 * mm, 210 * mm, 297 * mm)
#                     c.drawString(10 * mm, 290 * mm, pdf_name)
#                     c.showPage()
#                     os.remove(pic_path1)
#                 c.save()
#
# # 替换为你的PDF文件路径和输出路径
# input_pdf_path = r"C:\Users\Administrator\Desktop\demo\新建文件夹"
# output_pdf_path = r"C:\Users\Administrator\Desktop\demo\保存"
# pic_path = r'C:\Users\Administrator\Desktop\demo\空文件夹'
# try:
#     add_filename_to_pdf_content(input_pdf_path, output_pdf_path, pic_path)
# except Exception as e:
#     print(e)
#     traceback.print_exc()

# def add_filename_to_pdf_content(pdf_path, output_path, pic_path):
#     pdfmetrics.registerFont(TTFont('SimHei', 'SimHei.TTF'))
#     for root, dirs, files in os.walk(pdf_path):
#         for file in files:
#             if file.endswith('.pdf'):
#                 src_path = os.path.join(root, file)
#                 des_path = src_path.replace(pdf_path, output_path, 1)
#                 c = canvas.Canvas(des_path)
#                 pdf_name = file.strip('.pdf')
#                 src_pdf_reader = fitz.Document(src_path)
#                 is_first_page = True  # 标志变量，用于判断是否是第一页
#                 for pg in range(src_pdf_reader.page_count):
#                     page = src_pdf_reader.load_page(pg)  # 获得每一页的对象
#                     trans = fitz.Matrix(3.0, 3.0).prerotate(0)
#                     pm = page.get_pixmap(matrix=trans, alpha=False, dpi=200)
#                     pic_path1 = os.path.join(pic_path, f'{pdf_name}-{str(pg)}.jpg')
#                     pm.save(pic_path1)
#                     c.setPageSize(A4)
#                     c.setFont('SimHei', 12)
#                     c.drawImage(pic_path1, 0 * mm, 0 * mm, 210 * mm, 297 * mm)
#                     if is_first_page:
#                         c.drawString(10 * mm, 290 * mm, pdf_name)
#                         is_first_page = False  # 将标志变量设为False，以确保只在第一页添加文件名
#                     c.showPage()
#                     os.remove(pic_path1)
#                 c.save()
#
# # 替换为你的PDF文件路径和输出路径
# input_pdf_path = r"C:\Users\86130\Desktop\新建文件夹"
# output_pdf_path = r"C:\Users\86130\Desktop\新建文件夹\保存"
# pic_path = r'C:\Users\86130\Desktop\新建文件夹\pic'
# try:
#     add_filename_to_pdf_content(input_pdf_path, output_pdf_path, pic_path)
# except Exception as e:
#     print(e)
#     traceback.print_exc()