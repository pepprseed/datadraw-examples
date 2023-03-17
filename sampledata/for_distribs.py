
data1 = [ 33, 36, 39, 41, 41, 49, 53, 58, 61, 63, 65, 67, 69, 69, 71, 73, 76, 77, 78, 79, 82, 86, 87, 87, 88, 89, 
       89, 89, 90, 90, 92, 93, 93, 93, 93, 93, 96, 96, 96, 97, 97, 100, 100, 100, 100, 102, 102, 102, 103, 103, 
       103, 103, 104, 104, 105, 105, 106, 106, 107, 108, 108, 109, 109, 110, 112, 112, 113, 113, 113, 113, 114, 
       114, 114, 115, 116, 116, 118, 118, 119, 119, 119, 119, 120, 120, 120, 120, 121, 123, 123, 124, 124, 125, 
       125, 125, 126, 126, 127, 127, 128, 129, 129, 130, 130, 131, 131, 131, 131, 132, 133, 134, 134, 134, 135, 
       135, 136, 137, 137, 137, 137, 137, 138, 138, 138, 138, 138, 139, 139, 141, 141, 141, 142, 142, 142, 143, 
       145, 145, 146, 147, 147, 147, 148, 148, 148, 149, 150, 150, 151, 151, 151, 151, 151, 151, 151, 152, 153, 
       154, 155, 158, 159, 159, 161, 161, 161, 163, 163, 163, 163, 164, 164, 165, 165, 167, 169, 173, 174, 175, 
       175, 176, 176, 177, 178, 179, 181, 185, 185, 188, 194, 197, 199, 199, 207, 234, 265, 293, 309, 525 ]

data2 = [ 35, 47, 51, 51, 52, 52, 56, 59, 62, 62, 62, 62, 64, 65, 67, 69, 72, 72, 73, 73, 75, 75, 76, 76, 79, 79, 
       80, 80, 81, 84, 85, 86, 86, 86, 88, 88, 91, 92, 92, 94, 94, 98, 99, 100, 100, 101, 102, 102, 103, 103, 
       104, 105, 105, 106, 107, 107, 107, 109, 110, 110, 111, 111, 111, 111, 113, 113, 113, 113, 114, 114, 115, 
       115, 115, 115, 115, 116, 116, 116, 117, 117, 117, 117, 118, 119, 119, 121, 121, 121, 122, 122, 123, 123, 
       124, 125, 125, 125, 127, 127, 128, 128, 128, 129, 129, 130, 130, 130, 130, 131, 132, 132, 133, 133, 134, 
       134, 135, 136, 137, 137, 139, 139, 139, 139, 140, 140, 140, 140, 141, 141, 141, 142, 142, 143, 145, 146, 
       147, 147, 148, 148, 149, 151, 153, 155, 155, 156, 157, 158, 158, 162, 162, 163, 163, 164, 167, 169, 170, 
       170, 171, 172, 173, 174, 175, 176, 176, 177, 177, 184, 185, 186, 186, 187, 188, 189, 189, 190, 193, 223, 
       234, 260 ]

data3 = [ 9, 15, 27, 28, 36, 38, 40, 41, 44, 45, 45, 50, 52, 53, 53, 55, 56, 56, 59, 60, 60, 61, 62, 63, 63, 65, 70, 
       70, 71, 71, 72, 73, 74, 75, 76, 76, 77, 77, 78, 80, 81, 83, 83, 84, 85, 85, 86, 86, 87, 87, 88, 88, 88, 
       89, 89, 90, 91, 91, 92, 93, 94, 94, 94, 96, 96, 96, 97, 97, 99, 99, 99, 100, 100, 100, 101, 103, 105, 106, 
       107, 108, 108, 110, 111, 111, 114, 115, 115, 116, 116, 118, 118, 119, 120, 120, 121, 121, 122, 122, 122, 
       122, 124, 124, 125, 125, 128, 128, 129, 129, 130, 130, 131, 131, 134, 136, 137, 138, 138, 139, 140, 140, 
       140, 141, 143, 145, 145, 145, 146, 146, 148, 150, 152, 155, 156, 157, 159, 160, 161, 163, 164, 164, 164, 
       164, 165, 167, 168, 177, 178, 187, 187, 188, 189, 191, 193, 195, 199, 202, 208, 217, 237, 242, 254, 264, 
       282, 299, 313, 539, 556 ]

data4 = [ 16, 21, 22, 25, 29, 32, 32, 33, 34, 42, 43, 44, 44, 44, 45, 45, 46, 46, 48, 48, 48, 49, 51, 53, 53, 56, 
       56, 57, 58, 60, 60, 62, 63, 63, 66, 66, 66, 67, 68, 70, 70, 70, 70, 71, 72, 72, 72, 72, 72, 74, 75, 75, 
       75, 76, 76, 77, 80, 80, 82, 84, 85, 86, 86, 86, 86, 86, 87, 87, 87, 88, 88, 89, 89, 89, 90, 90, 91, 91, 
       92, 93, 94, 94, 95, 98, 98, 99, 100, 100, 100, 100, 102, 103, 103, 103, 105, 106, 107, 107, 107, 108, 
       108, 109, 109, 109, 109, 111, 113, 113, 113, 114, 114, 114, 115, 115, 116, 117, 118, 118, 119, 119, 120, 
       122, 122, 123, 124, 125, 125, 125, 127, 127, 129, 131, 132, 132, 133, 135, 137, 140, 141, 142, 144, 147, 
       151, 151, 156, 158, 158, 164, 166, 174, 175, 175, 177, 178, 190, 206, 207, 216, 261, 349, 430, 495 ]

