#!/usr/bin/env python
# encoding: utf-8

import csv
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from decimal import Decimal
from datetime import date, datetime
from django.template.context import RequestContext
from sws_tags.sws_utils.common_utils import *
from sws_tags.sws_utils.messages import *
from sws_tags.sws_utils.cube import *
from sws_tags.sws_utils.pdf_utils import *

import traceback

# FOR EXCEL 
try:
	import cStringIO as StringIO
except ImportError:
	import StringIO

from xlsxwriter.workbook import Workbook

# FOR EXCEL GENERATING
import xlwt
ezxf = xlwt.easyxf

from sws_tags.sws_utils.common_utils import *
from sws_tags.sws_utils.messages import *
from sws_tags.sws_utils.cube import *

def getRedirectURL(param_export_file,request,dst_directory='/media'):
	''' Create a redirect URL depending on the request and wether it is secure or not'''
	if request is not None:
		redirect_url = request.get_host() + '/' +dst_directory + param_export_file['filename']#).replace('http://','https://')
		redirect_url = redirect_url.replace('//','/')
		if request.is_secure():
			redirect_url = 'https://' + redirect_url
		else:
			redirect_url = 'http://' + redirect_url
	else:	
		redirect_url = dst_directory + param_export_file['filename']

	return redirect_url

def rounding(cifra, digitos=0,format='Round_up'):
	"""Rutina par rounding de cifras decimales como para uso en contabilidad"""
	# Symmetric Arithmetic Rounding for decimal numbers
	if type(cifra) != decimal.Decimal:
		cifra = decimal.Decimal(str(cifra))


	if format == 'Default':
		result = cifra.quantize(decimal.Decimal("1") / (decimal.Decimal('10') ** digitos), decimal.ROUND_HALF_UP)
	elif format == 'Round_up':
		result = cifra.quantize(decimal.Decimal("1") / (decimal.Decimal('10') ** digitos), decimal.ROUND_UP)	
	elif format == 'Round_down':
		result = cifra.quantize(decimal.Decimal("1") / (decimal.Decimal('10') ** digitos), decimal.ROUND_DOWN)	

	return result


def roundingBill(data,conf):

	new_data = []
	new_total = 0
	new_sum_minutes = 0

	for r in data:
		new_r = {}
		for i in r:
			if i not in conf:
				new_r[i] = r[i]
			elif i == 'sum_total_minutes':
				new_r[i] = rounding(r[i],conf[i][0],conf[i][1])


		for c in conf:
			if c == 'sum_total_income':
				new_sum_total_income = new_r['income'] * new_r['sum_total_minutes'] 
				new_r[c] = rounding(new_sum_total_income,conf[c][0],conf[c][1])

		new_data.append(new_r)
		new_total = new_total + new_r['sum_total_income']
		new_sum_minutes = new_sum_minutes + new_r['sum_total_minutes']


	sum_data = {}
	sum_data['sum_total_income'] = new_total
	sum_data['sum_total_minutes'] = new_sum_minutes

	return new_data,sum_data


def roundingBillIncome(data,conf):

	new_data = []
	new_total = 0
	new_sum_minutes = 0

	for r in data:

		new_r = {}
		for i in r:
			if i not in conf:
				new_r[i] = r[i]
			elif i == 'minutes':
				new_r[i] = rounding(r[i],conf[i][0],conf[i][1])

		for c in conf:
			if c == 'total_euro':
				new_total_euro = new_r['rate_euro'] * new_r['minutes'] 
				new_r[c] = rounding(new_total_euro,conf[c][0],conf[c][1])

		new_data.append(new_r)
		new_total = new_total + new_r['total_euro']
		new_sum_minutes = new_sum_minutes + new_r['minutes']

	sum_data = {}
	sum_data['total_euro'] = new_total
	sum_data['minutes'] = new_sum_minutes
	return new_data,sum_data



def ExportFile(param_export_file,request = None):
	def read_and_flush():
		output.seek(0)
		data = output.read()
		output.seek(0)
		output.truncate()
		return data

	def writeInStream():
			row = 0
			col = 0
			for h in headers:
				sheet.write(row, col, h,bold)
				col += 1
			row = 1
			col = 0
			for trr in queryset:
				for c in col_name:
					if type(trr[c]) == datetime:
						try:
							trr[c]=param_export_file['request_data']['django_timezone'].normalize(trr[c]).strftime('%Y-%m-%d %H:%M:%S')
						except:
							trr[c]=str(trr[c])
					sheet.write(row, col, trr[c])
					col += 1
				row += 1
				col = 0
				data = read_and_flush()
				yield data

			book.close()
			data = read_and_flush()
			yield data	


	def writeBillInStream():
		# //////////////////////////////////////////////   STYLE ///////////////////////////////////
		bold = book.add_format({'bold': 1})
		border = book.add_format({'bold': True,'font_color': 'green','border_color':'blue','border': 6})
		font_color_red = book.add_format({'bold': True,'color':'red'})
		yellow_bg = book.add_format({'bg_color':'#FFFFFF'})
		grey_bg = book.add_format({'bg_color':'#F7F7F7'})

		grey_dark_bg_bold = book.add_format({'bg_color':'#D7D6D2','bold':1})

		flesh_color_bg = book.add_format({'bg_color':'#FFE8E8'})
		flesh_color_bg_bold = book.add_format({'bg_color':'#FFE8E8','bold':1})

		merge_format_border = book.add_format({
		    'bold': 1,
		    'align': 'center',
		    'valign': 'vcenter',
		    'fg_color': '#FFE8E8',
		    # 'border': 1,
		    # 'border_color':'#8E0172',		    
		    })

		merge_format = book.add_format({
		    'bold': 1,
		    'align': 'center',
		    'valign': 'vcenter',
		    'fg_color': '#FFE8E8',
		    })


		red_format = book.add_format({
		    'bold': 1,
		    'align': 'center',
		    'valign': 'vcenter',
		    'fg_color': '#FFB3B3',
		    # 'border_color':'#FF3636',
		    # 'border':6
		    })


		money = book.add_format({'num_format': '#.##'+param_export_file['data_bill']['type_money'],'bold':1})

		money_grey_bg = book.add_format({'num_format': '#.##'+param_export_file['data_bill']['type_money'],'bold':1,'bg_color':'#F7F7F7'})
		money_grey_bg_0 = book.add_format({'num_format': '0.####'+param_export_file['data_bill']['type_money'],'bold':1,'bg_color':'#F7F7F7'})
		
		money_yellow_bg = book.add_format({'num_format': '#.####'+param_export_file['data_bill']['type_money'],'bold':1,'bg_color':'#FBE067'})
		money_yellow_bg_0 = book.add_format({'num_format': '0.####'+param_export_file['data_bill']['type_money'],'bold':1,'bg_color':'#FBE067'})


		minute_grey_bg = book.add_format({'num_format': '#.#','bg_color':'#F7F7F7'})
		minute_grey_bg_0 = book.add_format({'num_format': '0.#','bg_color':'#F7F7F7'})
		
		minute_yellow_bg = book.add_format({'num_format': '#.#','bg_color':'#FBE067'})
		minute_yellow_bg_0 = book.add_format({'num_format': '0.#','bg_color':'#FBE067'})

		
		date_format = book.add_format({'num_format': 'mmmm d yyyy'})
		# italic = book.add_format({'italic': True})


		# ///////////////////////////////////////////    DECLARATION /////////////////////////////////////////////
		pattern = xlwt.Pattern() # Create the Pattern 
		pattern.pattern = xlwt.Pattern.SOLID_PATTERN
		pattern_fore_colour = 5

		style = xlwt.XFStyle() # Create the Pattern 
		style.pattern = pattern 
		
		queryset = param_export_file['data_bill']['raw_cdrts'] 
		total = param_export_file['data_bill']['cdrt_subtotal']

		col_name = ['destination','minutes','rate_euro','total_euro']
		headers = ['Destination','Total Minutes','EUR/min','Total']


		sheet.set_column('A:A', 5)
		sheet.set_column('B:B', 30)
		sheet.set_column('C:C', 15)
		sheet.set_column('D:D', 15)
		sheet.set_column('E:E', 15)		


		sheet.set_column('G:G', 15)


		try:
			sheet.write(1,1,param_export_file['data_bill']['issuing_company_name'],bold)
			sheet.write(2,1,param_export_file['data_bill']['issuing_company_address'],bold)
			sheet.write(3,1,param_export_file['data_bill']['issuing_company_CIF'],bold)
			sheet.insert_image('A1',param_export_file['data_bill']['url_img'],{'x_offset':260,'y_offset':15})
			sheet.merge_range('D2:E4', 'BILL: '+param_export_file['data_bill']['invoice_number'], red_format)
		except:
			pass
			# print traceback.format_exc()
		

		# ///////////////////////////////////////  BILL /////////////////////////////////////////////
		row = 5
		col = 1
		for h in headers:
			sheet.write(row, col, h,grey_dark_bg_bold)
			col += 1
		row = 6
		col = 1

		col_max=len(col_name)


		for trr in queryset:
			for c in col_name:
				# print c
				if type(trr[c]) == datetime:
					try:
						trr[c]=param_export_file['request_data']['django_timezone'].normalize(trr[c]).strftime('%Y-%m-%d %H:%M:%S')
					except:
						# print traceback.format_exc()
						trr[c]=str(trr[c])

				# print 'aaaaaaaa',trr[c]

				if row%2 !=0:
					

					# if c == '' or  c == 'total_euro' :
					# 	if trr[c]>=1:
					# 		sheet.write(row,col,trr[c],money_yellow_bg)
					# 	else:
					# 		sheet.write(row,col,trr[c],money_yellow_bg_0)
					# elif c == 'minutes':
					# 	if trr[c]>=1:
					# 		sheet.write(row,col,trr[c],minute_yellow_bg)
					# 	else:
					# 		sheet.write(row,col,trr[c],minute_yellow_bg_0)				

					# else:
					# 	sheet.write(row, col, trr[c],yellow_bg)


					sheet.write(row, col, trr[c],yellow_bg)


				else:
					# if c == '' or  c == 'total_euro' :
					# 	if trr[c]>=1:
					# 		sheet.write(row,col,trr[c],money_grey_bg)
					# 	else:
					# 		sheet.write(row,col,trr[c],money_grey_bg_0)

					# elif c == 'minutes':
					# 	if trr[c]>=1:
					# 		sheet.write(row,col,trr[c],minute_grey_bg)
					# 	else:
					# 		sheet.write(row,col,trr[c],minute_grey_bg_0)		

					# else:
						# sheet.write(row,col,trr[c],grey_bg)

					sheet.write(row,col,trr[c],grey_bg)

				col += 1
			row += 1
			col = 1
			data = read_and_flush()
			yield data


		# /////////////////////////////////////////////// TOTAL ////////////////////////////////////////

		row = row+1
		sheet.write(row, col_max-3, 'Total Minutes',grey_bg)	
		sheet.write(row, col_max-2, total['minutes'],grey_bg)	
		sheet.write(row, col_max-1, 'Total',grey_bg)
		sheet.write(row, col_max, total['total_euro'],money_grey_bg)	

		row = row+1
		sheet.write(row, col_max-1,'IVA '+ str(param_export_file['data_bill']['VAT']) +'%',grey_bg)
		iva = float(total['total_euro']) * float(param_export_file['data_bill']['VAT'])/100

		sheet.write(row, col_max,iva,money_grey_bg)

		row = row+1
		sheet.write(row, col_max-1,'Total + IVA',money_grey_bg)
		total_iva = float(total['total_euro']) * (1 + float(param_export_file['data_bill']['VAT'])/100)
		sheet.write(row, col_max,total_iva,money_grey_bg)



		# /////////////////////////////////////////////  FOOTER DATA ////////////////////////////////////////
		row = row +3
		
		# print 'row-->',row
		# print 'col-->',col_max

		coordinate = 'B'+str(row)+':E'+str(row)
		period = 'Issue Date: '+ str(param_export_file['data_bill']['issue_date'])+ '      Due Date: '+str(param_export_file['data_bill']['due_date'])
		sheet.merge_range(coordinate, period, merge_format_border)

		row = row +2

		coordinate = 'B'+str(row)+':E'+str(row)
		period = 'Period From: '+ str(param_export_file['data_bill']['from_date'])+ '      Period To: '+str(param_export_file['data_bill']['to_date'])
		sheet.merge_range(coordinate, period, merge_format_border)

		row = row +2

		coordinate = 'B'+str(row)+':E'+str(row)
		period = 'Payment info for client: '+ str(param_export_file['data_bill']['payment'] )
		sheet.merge_range(coordinate, period, merge_format)

		row = row-1

		sheet.write(row+1, 1, 'Bank Name:',flesh_color_bg_bold)	
		sheet.write(row+2, 1, 'Account:',flesh_color_bg_bold)
		sheet.write(row+3, 1, 'IBAN:',flesh_color_bg_bold)	
		sheet.write(row+4, 1, 'SWIFT:',flesh_color_bg_bold)
		# sheet.write(row+3, 1, 'Beneficiary:',flesh_color_bg_bold)
		# sheet.write(row+4, 1, 'Bank addres:',flesh_color_bg_bold)

		sheet.write(row+1, 2, param_export_file['data_bill']['bank_name'],flesh_color_bg)	
		sheet.write(row+2, 2, param_export_file['data_bill']['account'],flesh_color_bg)
		sheet.write(row+3, 2, param_export_file['data_bill']['IBAN'],flesh_color_bg)	
		sheet.write(row+4, 2, param_export_file['data_bill']['SWIFT'],flesh_color_bg)
		# sheet.write(row+3, 2, param_export_file['data_bill']['beneficiary'],flesh_color_bg)
		# sheet.write(row+4, 2, param_export_file['data_bill']['bank_addres'],flesh_color_bg)



		sheet.write(row+1, 3, 'Company:',flesh_color_bg_bold)
		sheet.write(row+2, 3, 'CIF:',flesh_color_bg_bold)
		sheet.write(row+3, 3, 'Adress:',flesh_color_bg_bold)
		sheet.write(row+4, 3, 'Email:',flesh_color_bg_bold)	
		sheet.write(row+5, 3, 'Phone:',flesh_color_bg_bold)

		sheet.write(row+1, 4, param_export_file['data_bill']['company'],flesh_color_bg)
		sheet.write(row+2, 4, param_export_file['data_bill']['company_number'],flesh_color_bg)
		sheet.write(row+3, 4, param_export_file['data_bill']['company_address'],flesh_color_bg)
		sheet.write(row+4, 4, param_export_file['data_bill']['company_email'],flesh_color_bg)
		sheet.write(row+5, 4, param_export_file['data_bill']['company_phone'],flesh_color_bg)



		book.close()

		data = read_and_flush()
		yield data	



	if param_export_file['format'] == 'excel':

		param_export_file['file'] = False

		if param_export_file['file'] == True:

			param_export_file['filename'] = param_export_file['filename']+'_' + str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))+'.xlsx'

			queryset = param_export_file['queryset']
			headers = param_export_file['headers']
			col_name = param_export_file['col_name']
			filename = param_export_file['filename']
			logger = param_export_file['logger']

			output = StringIO.StringIO()

			book = Workbook(output)
			sheet = book.add_worksheet('test') 

			bold = book.add_format({'bold': 1})
			response = HttpResponse(writeInStream(), mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
			response['Content-Disposition'] = "attachment; filename="+ filename
			return response
		
		else:
			param_export_file['filename'] = param_export_file['filename']+'_' + str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))+'.xlsx'

			queryset = param_export_file['queryset']
			headers = param_export_file['headers']
			col_name = param_export_file['col_name']
			filename = param_export_file['filename']
			logger = param_export_file['logger']

			try:

				filename = param_export_file['STATIC_URL'] +'/excel_csv/'+ param_export_file['filename']

				book = Workbook(filename,{'constant_memory': True})
				sheet = book.add_worksheet('test') 
				bold = book.add_format({'bold': 1})

				col = 0
				row = 0
				for h in headers:
						sheet.write(row, col, h,bold)
						col += 1
				row = 1
				col = 0

				# if type(queryset) == list:
				# 	pass
				# else:
				# 	queryset=queryset.iterator()



				for trr in queryset:
					for c in col_name:
						if c in trr:
							if type(trr[c]) == datetime:
								try:
									trr[c]=param_export_file['request_data']['django_timezone'].normalize(trr[c]).strftime('%Y-%m-%d %H:%M:%S')
								except:
									trr[c]=str(trr[c])

							sheet.write(row, col, trr[c])
						col += 1
					row += 1
					col = 0
				book.close()

			except:
				print 'ERROR-->',traceback.format_exc()

			redirect_url = getRedirectURL(param_export_file,request, '/media/excel_csv/')

			response = HttpResponseRedirect(redirect_url)
			return response
		

	elif param_export_file['format'] == 'csv':
		# param_export_file['filename'] = param_export_file['filename']+'_'+str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
		param_export_file['filename'] = param_export_file['filename']+'_'+str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))+'.csv'
		try:
			col_name = param_export_file['col_name']
		except:
			col_name =None

		json_data = get_csv_query(param_export_file['request_data'], param_export_file['queryset'], param_export_file['STATIC_URL'] +'/excel_csv/'+ param_export_file['filename'],col_name)
		# response = HttpResponse(json_data, mimetype='text/csv') 
		# param_export_file['filename'] += '.csv'
		# response['Content-Disposition'] = 'attachment; filename=' + param_export_file['filename']
		

		redirect_url = getRedirectURL(param_export_file,request,'/media/excel_csv/')

		response = HttpResponseRedirect(redirect_url)

		return response

	elif param_export_file['format'] == 'bill':

		param_export_file['filename'] = param_export_file['filename']+'_' + str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))+'.xlsx'
		filename = param_export_file['filename']
		logger = param_export_file['logger']

		output = StringIO.StringIO()

		book = Workbook(output)
		sheet = book.add_worksheet('test') 

		book.set_properties({
			'title':    param_export_file['filename'],
			'subject':  'Bill',
			'author':   param_export_file['autor'],
			'manager':  'StoneWorkSolutions',
			'company':  'StoneWorkSolutions',
			'category': 'Bill and risk',
			'keywords': 'Bill',
			'comments': 'Created in portal international'})

		response = HttpResponse(writeBillInStream(), mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
		response['Content-Disposition'] = "attachment; filename="+ filename
		return response

	elif param_export_file['format']=='bill_pdf':
		# return render_to_response('tags/pdf_format.html', dictionary=None, context_instance=param_export_file)
		req=ThreadLocal.get_current_request()
		rc = RequestContext(req)
		for k,v in param_export_file.iteritems():
			rc[k]=v
		# return render_to_pdf('tags/pdf_format.html', dictionary=None, context_instance=param_export_file, header_template=None, footer_template='tags/tag_footer.html', filename=param_export_file['filename'])
		return render_to_pdf('tags/pdf_format.html', dictionary=None, context_instance=rc, header_template=None, footer_template='tags/tag_footer.html', filename=param_export_file['filename'])




def get_csv_query(request, queryset, filename, col_order = None,in_stream=False):

	kind_to_xf_map = {
		'date': ezxf(num_format_str='yyyy-mm-dd HH:MM'),
		'int': ezxf(num_format_str='#,##0'),
		'money': ezxf('font: italic on; pattern: pattern solid, fore-colour grey25',
			num_format_str='€#,##0.00'),
		'price': ezxf(num_format_str='#0.000'),
		'text': ezxf(),
		'boolean': ezxf(),
	}

	try:
		if in_stream==False:
			csv_file = open(filename,"w")
		else:
			csv_file = HttpResponse()

		csv_writer = csv.writer(csv_file, dialect='excel', quoting=csv.QUOTE_MINIMAL, delimiter='|')

		if type(queryset)!=list:
			q = queryset[0]

			
			fields = []
			for f in queryset._fields:
				fields.append(q[f])
			for f in queryset.aggregate_names:
				fields.append(q[f])

			fields_name = []
			for f in queryset._fields:
				fields_name.append(unicode(getFieldVerboseName(queryset,f)))
			for f in queryset.aggregate_names:
				fields_name.append(f)


			data_xfs_types_used = [k for k in get_field_types(fields)]
			data_xfs = [kind_to_xf_map[k] for k in get_field_types(fields)]

			data = []


			for i, q in enumerate(queryset):
				aux = []
				i=0
				for f in queryset._fields:

					if data_xfs_types_used[i] == 'date':
						try:
							date_normalize=request['django_timezone'].normalize(q[f]).strftime('%Y-%m-%d %H:%M:%S')
							aux.append(str(date_normalize))
						except:
							# print traceback.format_exc()
							aux.append(q[f])

					else:
						aux.append(q[f])
					i+=1
				for f in queryset.aggregate_names:
					aux.append(q[f])
				data.append(aux)

		else:
			fields_name = []
			if col_order:
				fields_name=col_order
			else:
				for k,v in queryset[0].items():
					fields_name.append(unicode(k))

			data = []

			# print fields_name

			for q in queryset:
				v_data=[]
				for k in fields_name:
					if k in q:
						v_data.append(q[k])
				data.append(v_data)
		csv_writer.writerow(fields_name)

		for row in data:
			csv_writer.writerow(row)							
								
		# csv_file.close()
		return csv_file

	except Exception, e:
		swslog('error','get_csv_query',e)
		return False


def get_field_types(fields):
	# fields = self.fields
	field_types = []
	prev_len = 0
	found = False
	for lf in fields:
		found = False
		if type(lf) == unicode:
			field_types.append('text')
			found = True
		elif type(lf) == long:
			field_types.append('int')
			found = True
		elif type(lf) == int:
			field_types.append('int')
			found = True
		elif type(lf) == bool:
			field_types.append('boolean')
			found = True
		elif type(lf) == float: 
			field_types.append('price')
			found = True
		elif type(lf) == Decimal: 
			field_types.append('price')
			found = True                    
		elif type(lf) == date:
			field_types.append('date')
			found = True                
		elif type(lf) == datetime: 
			field_types.append('date')
			found = True              
		if found is not True: 
			field_types.append('text')
	return field_types












# def ExportFile_STYLE(param_export_file): # STYLE

# 	if param_export_file['format'] == 'excel':

# 		param_export_file['filename'] = param_export_file['filename']+'_' + str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))+'.xlsx'

# 		queryset = param_export_file['queryset']
# 		headers = param_export_file['headers']
# 		col_name = param_export_file['col_name']
# 		filename = param_export_file['filename']
# 		logger = param_export_file['logger']


# 		# styles = dict(
# 		#     bold = 'font: bold 1',
# 		#     italic = 'font: italic 1',
# 		#     # Wrap text in the cell
# 		#     wrap_bold = 'font: bold 1; align: wrap 1;',
# 		#     # White text on a blue background
# 		#     reversed = 'pattern: pattern solid, fore_color blue; font: color white;',
# 		#     # Light orange checkered background
# 		#     light_orange_bg = 'pattern: pattern fine_dots, fore_color white, back_color orange; font: bold 1; align: wrap 1;',
# 		#     # Heavy borders
# 		#     bordered = 'border: top thick, right thick, bottom thick, left thick;',
# 		#     # 16 pt red text
# 		#     big_red = 'font: height 320, color orange;',
# 		# )



# 		book = xlwt.Workbook()
# 		sheet = book.add_sheet('file_xlsx')
# 		style = xlwt.easyxf('pattern: pattern fine_dots, fore_color white, back_color orange; font: bold 1; align: wrap 1;')
# 		style_content = xlwt.easyxf('font: bold 1')


# 		# wb = Workbook()
# 		# ws = wb.get_active_sheet()
# 		# ws.title = filename


# 		row = 0
# 		col = 0
# 		for h in headers:
# 			sheet.write(row, col, h, style)
# 			# cell = ws.cell(row = row, column = col)
# 			# cell.value = h
# 			# cell.style = style
# 			# printº 'zzzzzzzzzzzzzzzzz',cell
# 			col += 1
	
# 		row = 1
# 		col = 0
# 		for trr in queryset:
# 			for c in col_name:
# 				# cell = ws.cell(row = row, column = col)
# 				sheet.write(row, col, trr[c])
# 				col += 1
# 				# cell.value = trr[c]

				

# 			row += 1
# 			col = 0

# 		# response = HttpResponse(mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') 		
# 		# response['Content-Disposition'] = 'attachment; filename='+filename
# 		# wb.save(response)

# 		# response = HttpResponse(mimetype="application/ms-excel")
# 		# response['Content-Disposition'] = 'attachment; filename= test.xls'
# 		book.save(response)

# 		return response

# 	elif param_export_file['format'] == 'csv':
# 		param_export_file['filename'] = param_export_file['filename']+'_'+str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))

# 		json_data = get_csv_query(param_export_file['request_data'], param_export_file['queryset'], param_export_file['filename'])
# 		response = HttpResponse(json_data, mimetype='text/csv') 
# 		param_export_file['filename'] += '.csv'
# 		response['Content-Disposition'] = 'attachment; filename=' + param_export_file['filename']
# 		return response


# def ExportFileSaveinstream(param_export_file):
# 	if param_export_file['format'] == 'excel':
# 		param_export_file['filename'] = param_export_file['filename']+'_' + str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))+'.xlsx'

# 		queryset = param_export_file['queryset']
# 		headers = param_export_file['headers']
# 		col_name = param_export_file['col_name']
# 		filename = param_export_file['filename']
# 		logger = param_export_file['logger']

# 		response = HttpResponse(mimetype='application/ms-excel') 		
# 		response['Content-Disposition'] = 'attachment; filename='+filename


# 		wb = Workbook()
# 		ws = wb.get_active_sheet()
# 		ws.title = filename

# 		row = 0
# 		col = 0
# 		for h in headers:
# 			cell = ws.cell(row = row, column = col)
# 			cell.value = h
# 			col += 1
	
# 		row = 1
# 		col = 0

# 		wb.save(response)
# 		for trr in queryset:
# 			for c in col_name:
# 				cell = ws.cell(row = row, column = col)
# 				col += 1
# 				cell.value = trr[c]

# 			wb.save(response)
# 			row += 1
# 			col = 0

# 		wb.save(response)
# 		return response
