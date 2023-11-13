import glob
import os
import cv2
import numpy as np
import sys

def crop_image(image, border_size):
    if image is None:
        print("Error: Unable to read the input image.")
        return

    # Get image dimensions
    height, width, channels = image.shape

    # Calculate the new dimensions after reducing the border size
    new_height = height - 2 * border_size
    new_width = width - 2 * border_size

    if new_height <= 0 or new_width <= 0:
        print("Error: Border size is too large for the input image.")
        return

    # Crop the image
    cropped_image = image[border_size:height-border_size, border_size:width-border_size]

    ## # Display or save the cropped image
    ## cv2.imshow("Cropped Image", cropped_image)
    ## cv2.waitKey(0)
    ## cv2.destroyAllWindows()
    return cropped_image

def detect_and_remove_dark_borders(image, threshold=10, contour_reduction=0):
    # Convertir l'image en niveaux de gris
    gray = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY)

    _,thresh = cv2.threshold(gray,1,255,cv2.THRESH_BINARY)
    contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    ## # Appliquer un flou gaussien pour réduire le bruit
    ## blurred = cv2.GaussianBlur(gray, (5, 5), 0)
## 
    ## cv2.imwrite(basename, blurred)

    ### Utiliser la détection de contour de Canny
    ##edges = cv2.Canny(blurred, threshold, threshold * 2)
##
    ### Trouver les contours dans l'image
    ##contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Si des contours sont trouvés, supprimer les bords sombres
    if len(contours) > 0:
        max_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(max_contour)

        # Réduire la taille du contour maximal
        x += contour_reduction
        y += contour_reduction
        w -= 2 * contour_reduction
        h -= 2 * contour_reduction        

        # Recadrer l'image pour supprimer le cadre sombre
        cropped_image = image[y:y+h, x:x+w]

        return cropped_image

    return image

## if __name__ == "__main__":
## if len(sys.argv) != 3:
##     print("Utilisation : python script.py nom_de_l_image.jpg contour_reduction")
## else:
##     image_filename = sys.argv[1]
##     contour_reduction = int(sys.argv[2])
##     image = cv2.imread(image_filename)
## 
##     if image is not None:
##         new_image = detect_and_remove_dark_borders(image, contour_reduction=contour_reduction)
## 
##         # Créer le nom du fichier de sortie avec le suffixe "nobords" et la valeur de contour_reduction
##         output_filename = image_filename.replace(".jpg", f"_nobords_{contour_reduction}.jpg")
##         cv2.imwrite(output_filename, new_image)
## 
##         print(f"Image avec cadre sombre supprimé enregistrée sous le nom : {output_filename}")
##     else:
##         print(f"L'image {image_filename} n'a pas pu être chargée.")


import shutil

coversNoBordersDir = 'covers-no-border'
shutil.rmtree(coversNoBordersDir, ignore_errors=True)
os.makedirs(coversNoBordersDir)


extensions = ['jpg', 'jpeg', 'webp', 'png']
for ext in extensions:
    # for image_filename in glob.iglob('thumbs/*.'+ext, recursive=True):
    for image_filename in glob.iglob('covers/*.'+ext, recursive=True):

        basename = os.path.basename(image_filename)
        newName = f"{coversNoBordersDir}/{basename}"
        # grayName = f"{coversNoBordersDir}/N_{basename}.gray.jpg"
        if not os.path.isfile(newName):
          image = cv2.imread(image_filename)
    
          if image is not None:

            new_image = detect_and_remove_dark_borders(image)
            # img_rgb = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
            # new_image = crop_image(image, 12)
            cv2.imwrite(newName, new_image)
            print(newName)
                    