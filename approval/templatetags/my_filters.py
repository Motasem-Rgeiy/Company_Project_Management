from django import template
from project.models import ProjectStatus
from blog.models import PostStatus

register = template.Library()

def title_cut(title):
    print('Here is tamplet tags')
    if not title:
        return 'Untitled'
    if len(title) <= 20:
        return title
    
    return title[:20] + '. '*15

def profile_name_cut(name):
    if not name:
        return 'Unnamed'
    if len(name) <= 5:
        return name

    return name[:5] + '..'


def get_post_status(status_num):
    return [
        status[1] for status in PostStatus.choices
        if status[0] == status_num
    ][0]



def get_project_status(status_num):
    print(ProjectStatus.choices)
    return [
            status[1] for status in ProjectStatus.choices
            if status[0] == status_num
        ][0]
    


register.filter('cut' , title_cut)
register.filter('cut_name', profile_name_cut)
register.filter('post_status_name', get_post_status)
register.filter('project_status_name', get_project_status)
