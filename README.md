# imagedb

Imagedb is a server side file management that can help you secure, store and manage up to one trillion images.

To store, retrieve or delete images you need to set up your auth key so you can have access to the images path (setting auth key is possible only when you first initialize the imagedb for the first time).

Passing an image path to the push("C:/user/users/xxx.png") method will return an id path as a string like "1:1:1:1:1:png" that you can store in your database as a reference to that image path.

If you pass an id path like "1:1:1:1:1:png" to the getpath("1:1:1:1:1:png") method you will receive the full path of the image that Imagedb store for you.

###How files are managed in imagedb?

The _Trillion_ folder contains 1000 _Billion_ folder.
The _Billion_ folder contains 1000 _Million_ folder.
The _Million_ folder contains 1000 _Thousand_ folder.
The _Thousand_ folder contains 1000 imges.

###How to read the image id path?

"1:2:3:4:5:png" == _Trillion_1/_Billion_2/_Million_3/_Thousand_ 4/5.png

Note: the folders and images names are hashed, the first 20 character of the SHA-256.
