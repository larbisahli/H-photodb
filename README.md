# H-photodb

hpdb is a server side file management that can help you secure, store and manage up to one trillion images.
(Use this only if you don't need to have a manual access to your images.)

To store, retrieve and delete images you need to set up your auth key so you can have access to the images path (setting auth key is possible only when you first initialize the hpdb for the first time).

Passing an image path to the push method push(path="C:/user/users/xxx.png", name="user") will return an id path with the name you chose as a string like "1:1:1:1:1:png:user" that you can store in your database as a reference to that image path.

If you pass an id path like "1:1:1:1:1:png:user" to the getpath method getpath("1:1:1:1:1:png:user") you will receive the full path of the image that Imagedb store for you.

full path look like : 

"C:\Users\User\Desktop\Imagedb\377837be7d08e9cc9f50\ce0f59c031b4df6de62c\b5d24a118aea2a99df8c\8c301d6ef3bac6b1b216\user_4523540f1504cd17100c.png"

### How files are managed in hpdb?

- The (T) directory contains 1000 (B) folders.
- The (B) directory contains 1000 (M) folders.
- The (M) directory contains 1000 (Th) folders.
- The (Th) directory contains 1000 images.
that are created on need.

### How to read the image id path?

> "1:2:3:4:5:png:user" == _T_1/_B_2/_M_3/_Th_4/user_5.png

Note: the folders and images names are hashed except for the name (user), the first 20 characters of the SHA-256.
