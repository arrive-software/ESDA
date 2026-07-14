# ESDA
ESDA (Easy Snake Descent Algorithm) is a simple symmetric encryption algorithm inspired by AES. The encryption process of ESDA 4x4 operates on a 4x4 numerical matrix.
[Click to see the principle](https://arrive-software.github.io/2025/03/07/%E8%BE%BE%E5%93%A5%E9%9B%86%E5%9B%A2%E5%9F%BA%E6%9C%AC%E5%8A%A0%E5%AF%86%E5%8D%8F%E8%AE%AE/)

### The way to use  
--- 
#### esda
Import esda as a module.ESDA provides six functions which include esda() unesda() text_to_matrices() matrices_to_text() encrypt_text() decrypt_text().

> esda()

ESDA requires two 4×4 matrices as parameters (which are mandatory). The first one serves as the plaintext, and the second one serves as the key for the ESDA computation.  
Then it output the encrypted matrix.

> unesda()

Similar to ESDA, the former is the encrypted matrix, and the latter is the key.

Then it output the decrypted matrix.

> text_to_matrices()

Only one parameters(text of arbitrary length).

This function outputs two values: the first is the input text converted to ASCII and then split into multiple 4×4 matrices, and the second is the number of matrices. (If the data is less than 16 elements, it is automatically padded with zeros.)

> matrices_to_text()

It requires two parameters.The first parameter is a matrice including one or more encrypted matrices.The second parameter is the length of origion matrix.

This function returns a string.

> encrypt_text()

This function takes two parameters: the first parameter is a string that serves as the plaintext, and the second parameter is a 4×4 matrix that serves as the key.

then return two value: The first is encrypted matrices and the second is the length of origin matrices.

> decrypt_text()

This function takes three parameters:The first is encrypted matrices,the second is the length of origin matrices and the final is the key matrix.

then return decrypted matrices.

#### fileesda

Interactively operate on the text file with the .esda extension, and read the first 16 characters from the key file as the key.

Generate a file with the .ae extension.

### web demo

[esda demo](https://arrive-software.github.io/2026/07/14/esdademo/)
