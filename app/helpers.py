from flask import render_template, request

def paged_object_list(template_name, query, paginate_by=20, **context):
  page = request.args.get('page')
  if page and page.isdigit():
      page = int(page)
  else:
      page = 1
  object_list = query.paginate(page, paginate_by)
  print(template_name)
  path_name = template_name.split('/')[-1]
  return render_template(template_name, object_list=object_list, the_path=path_name, **context)