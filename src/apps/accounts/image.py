from PIL import Image
import os
import settings
import shutil

__all__ = ('smart_thumb', 'smart_thumbEx', 'getImageNewFilename', 'copyFile',)

def smart_thumb(filename, to_width, to_height, crop=True):
    im = Image.open(filename)
    im.save(filename)
    
    from_width, from_height = im.size
    oldSize=im.size
    
    to_height = to_height or (to_width * from_height / from_width)

    if crop:
        ratio = min(float(from_width)/to_width, float(from_height)/to_height)
        crop_width_delta, crop_height_delta = int((from_width-ratio*to_width)/2), int((from_height-ratio*to_height)/2)
        im = im.crop((crop_width_delta, crop_height_delta, from_width-crop_width_delta, from_height-crop_height_delta))
    else:
        ratio = max(float(from_width)/to_width, float(from_height)/to_height)
        (to_width, to_height) = (from_width / ratio, from_height / ratio)
    
    im.thumbnail((to_width, to_height), Image.ANTIALIAS)
    im.save(filename)

#def smart_thumbEx(model, fieldName, to_width, to_height):
def smart_thumbEx(model, fieldName, to_width, to_height, crop=True):    
#    get_image_filename= getattr(model, ('get_%s_filename' % fieldName))
#    get_image_width= getattr(model, 'get_%s_width' % fieldName)
#    get_image_height= getattr(model, 'get_%s_height' % fieldName)
#    if get_image_filename() != '':
#        #print get_image_width(), '!=', to_width,' or ',get_image_height(),'!=', to_height
#        if get_image_width() != to_width or get_image_height() != to_height:
#            smart_thumb(get_image_filename(), to_width, to_height)
    #print model.cardImg.path
    #print getattr(model, fieldName)

    image_filename= os.path.join(settings.MEDIA_ROOT, getattr(model, fieldName).path)
    image_width= getattr(model, fieldName).width
    image_height= getattr(model, fieldName).height
    
    if image_filename != '':
        if image_width != to_width or image_height != to_height:
            smart_thumb(image_filename, to_width, to_height, crop=crop)
            

def getImageNewFilename(filename):
    # If the filename already exists, keep adding an underscore to the name of
    # the file until the filename doesn't exist.
    while os.path.exists(os.path.join(settings.MEDIA_ROOT, filename)):
        try:
            dot_index = filename.rindex('.')
        except ValueError: # filename has no dot
            filename += '_'
        else:
            filename = filename[:dot_index] + '_' + filename[dot_index:]
    return filename


def copyFile(filename, newFilename):
    #if newFilename=="":
    newFilename=getImageNewFilename(filename)
    shutil.copyfile(filename, newFilename)
    #print newFilename
    newFilename = newFilename[len(settings.MEDIA_ROOT)+1:]
    #print newFilename
#            
#            
#            import urlparse
#            print settings.MEDIA_ROOT
#            print urlparse.urljoin(settings.MEDIA_URL, self.card_img).replace('\\', '/')
    
    return newFilename
