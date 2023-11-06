# Converts an indented text or list of strings into a nested dictionary structure based on the indentation levels.


## pip install indent2dict


```python

Args:
	data (str, bytes, or list): The input data to be converted into a nested dictionary. It can be a string, bytes,
		or a list of strings.
	removespaces (bool): If True, leading and trailing whitespaces in the strings will be removed when constructing
		the dictionary keys. If False, whitespaces will be preserved.

Returns:
	dict: A nested dictionary structure where each level is determined by the indentation in the input data.
		The structure represents a hierarchy of items based on the indentation levels.

Example:
	input_data = [
		"Category 1",
		"  Subcategory 1.1",
		"    Item 1.1.1",
		"  Subcategory 1.2",
		"Category 2",
		"  Item 2.1",
	]

	result = indent2dict(input_data, removespaces=True)

	The 'result' will be:
	{
		'Category 1': {
			'Subcategory 1.1': {'Item 1.1.1': 0},
			'Subcategory 1.2': 1
		},
		'Category 2': {'Item 2.1':2}
	}


da2 = """      
      DecorView@479a814[HomeActivity]
        android.widget.LinearLayout{c7ad8bd V.E...... ......ID 0,0-1600,900}
          android.view.ViewStub{d860eb2 G.E...... ......I. 0,0-0,0 #102018a android:id/action_mode_bar_stub}
          android.widget.FrameLayout{a3aae03 V.E...... ......ID 0,0-1600,900 #1020002 android:id/content}
            android.widget.FrameLayout{5533180 V.E...... ......ID 0,0-1600,900}
              androidx.drawerlayout.widget.DrawerLayout{68143b9 VFE...... ......ID 0,36-1600,900 #7f0800af app:id/drawer_layout}
                com.bluestacks.launcher.widget.ItemOptionView{1c263fe VFED..... .F....ID 0,0-1600,864 #7f0800dd app:id/item_option}
                  androidx.constraintlayout.widget.ConstraintLayout{eb0275f V.E...... ......ID 0,0-1600,864}
                    android.widget.RelativeLayout{f79e5ac VFE...C.. ......ID 501,81-1100,130 #7f080133 app:id/searchRelativeLayout}
                      android.widget.ImageView{9e96275 V.ED..... ......ID 19,14-38,33 #7f080132 app:id/searchPlayIcon}
                      android.widget.ImageView{fdcc20a VFED..C.. ......ID 561,14-580,33 #7f080131 app:id/searchIcon}
                      android.widget.EditText{1d9da7b VFED..CL. ......ID 37,0-561,49 #7f080130 app:id/searchEditText}
                    com.bluestacks.launcher.widget.Desktop{75b098 VFED..... ......ID 44,166-1556,554 #7f08009c app:id/desktop}
                      com.bluestacks.launcher.widget.CellContainer{b7ab0f1 V.ED..... ......ID 0,0-1512,388}
                        d1.b{8cf4d6 VFED..CL. ........ 0,0-252,194}
                        d1.b{221a357 VFED..CL. ........ 252,0-504,194}
                        d1.b{4613e44 VFED..CL. ........ 504,0-756,194}
                        d1.b{af86b2d VFED..CL. ........ 756,0-1008,194}
                        d1.b{e3b8862 VFED..CL. ........ 1008,0-1260,194}
                        d1.b{25367c7 VFED..CL. ......I. 0,0-0,0}
                    com.bluestacks.launcher.widget.PagerIndicator{b31df3 I.ED..... ......ID 0,554-1600,570 #7f08009d app:id/desktopIndicator}
                    android.widget.LinearLayout{c55fab0 I.E...... ......ID 737,570-864,600 #7f0800d9 app:id/install_progress_layout}
                      android.widget.ProgressBar{71d8d29 V.ED..... ......ID 10,7-25,22 #7f0800ec app:id/loadingBar}
                      android.widget.TextView{f4dc8ae V.ED..... ......ID 35,4-117,25 #7f0800da app:id/installingGame}
                    android.widget.LinearLayout{bd7a64f V.E...... .......D 196,631-1404,864 #7f0800a5 app:id/dock}
                      android.widget.TextView{f9811dc V.ED..... ........ 0,9-1208,27 #7f080118 app:id/popular_gam}
                      android.widget.FrameLayout{558d2e5 V.E...... .......D 0,27-1208,233 #7f0800bb app:id/frameLayout}
                        android.view.View{931c1ba V.ED..... ......ID 0,90-1208,206 #7f08017b app:id/viewBackground}
                        android.widget.FrameLayout{312586b V.E...... .......D 0,0-1208,206}
                          android.widget.ProgressBar{3826fc8 G.ED..... ......I. 589,88-619,118 #7f0800a6 app:id/dockLoadingBar}
                          android.widget.LinearLayout{948b861 V.E...... .......D 62,-8-1146,182 #7f080048 app:id/allappsLinearLayout}
                            android.widget.LinearLayout{82a3f86 VFE...C.. .......D 66,0-225,190 #7f080050 app:id/appOneLinearLayout}
                              android.widget.FrameLayout{fc1047 V.E...... ......ID 29,34-129,134 #7f080058 app:id/app_image_one}
                                android.widget.ImageView{632c074 V.ED..... ......ID 74,3-97,26 #7f08011b app:id/popup_image_one}
                              android.widget.TextView{7f7799d V.ED..... ........ 0,142-159,190 #7f080060 app:id/app_name_one}
                            android.widget.LinearLayout{7dace12 VFE...C.. .......D 225,0-384,190 #7f080053 app:id/appTwoLinearLayout}
                              android.widget.FrameLayout{6df69e3 V.E...... ......ID 29,34-129,134 #7f08005b app:id/app_image_two}
                                android.widget.ImageView{7f56fe0 I.ED..... ......ID 74,3-97,26 #7f08011e app:id/popup_image_two}
                              android.widget.TextView{2d71299 V.ED..... ........ 0,142-159,190 #7f080063 app:id/app_name_two}
                            android.widget.LinearLayout{893b95e VFE...C.. .......D 384,0-543,190 #7f080052 app:id/appThreeLinearLayout}
                              android.widget.FrameLayout{614c13f V.E...... ......ID 29,34-129,134 #7f08005a app:id/app_image_three}
                                android.widget.ImageView{f71aa0c I.ED..... ......ID 74,3-97,26 #7f08011d app:id/popup_image_three}
                              android.widget.TextView{67d3f55 V.ED..... ........ 0,142-159,190 #7f080062 app:id/app_name_three}
                            android.widget.LinearLayout{d5e0d6a VFE...C.. .......D 543,0-702,190 #7f08004f app:id/appFourLinearLayout}
                              android.widget.FrameLayout{31e325b V.E...... ......ID 29,34-129,134 #7f080057 app:id/app_image_four}
                                android.widget.ImageView{4955af8 V.ED..... ......ID 74,3-97,26 #7f08011a app:id/popup_image_four}
                              android.widget.TextView{91f7bd1 V.ED..... ........ 0,142-159,190 #7f08005f app:id/app_name_four}
                            android.widget.LinearLayout{ec79636 VFE...C.. .......D 702,0-860,190 #7f08004e app:id/appFiveLinearLayout}
                              android.widget.FrameLayout{e839937 V.E...... ......ID 29,34-129,134 #7f080056 app:id/app_image_five}
                                android.widget.ImageView{e412ea4 I.ED..... ......ID 74,3-97,26 #7f080119 app:id/popup_image_five}
                              android.widget.TextView{4cf040d V.ED..... ........ 0,142-158,190 #7f08005e app:id/app_name_five}
                            android.widget.LinearLayout{e6edfc2 VFE...C.. .......D 860,0-1018,190 #7f080051 app:id/appSixLinearLayout}
                              android.widget.FrameLayout{f6e91d3 V.E...... ......ID 29,34-129,134 #7f080059 app:id/app_image_six}
                                android.widget.ImageView{eb49110 V.ED..... ......ID 74,3-97,26 #7f08011c app:id/popup_image_six}
                              android.widget.TextView{974d409 V.ED..... ........ 0,142-158,190 #7f080061 app:id/app_name_six}
                    com.bluestacks.launcher.widget.GroupPopupView{74f360e IFE...C.. ......ID 0,0-1600,864 #7f0800c2 app:id/groupPopup}
                      androidx.cardview.widget.CardView{6a0c61c I.E...... ......ID 0,0-647,406}
                        android.widget.LinearLayout{c06782f V.E...... ......ID 6,6-641,400}
                          android.widget.TextView{ab9ae3c VFED..C.. ........ 25,20-635,54 #7f0800c4 app:id/group_popup_label}
                          com.bluestacks.launcher.widget.CellContainer{28da7c5 I.ED..... ......ID 37,54-598,374 #7f0800c1 app:id/group}
                    android.view.View{6cca51a V.ED..... ......ID 44,166-82,554 #7f0800e3 app:id/leftDragHandle}
                    android.view.View{b8c684b V.ED..... ......ID 1518,166-1556,554 #7f080128 app:id/rightDragHandle}
                  com.bluestacks.launcher.widget.ItemOptionView$c{7917228 V.ED..... ........ 0,0-1600,864}"""

from indent2dict import indent2dict
conv = indent2dict(da2, removespaces=True)
print(conv)

{
    "DecorView@479a814[HomeActivity]": {
        "android.widget.LinearLayout{c7ad8bd V.E...... ......ID 0,0-1600,900}": {
            "android.widget.FrameLayout{a3aae03 V.E...... ......ID 0,0-1600,900 #1020002 android:id/content}": {
                "android.widget.FrameLayout{5533180 V.E...... ......ID 0,0-1600,900}": {
                    "androidx.drawerlayout.widget.DrawerLayout{68143b9 VFE...... ......ID 0,36-1600,900 #7f0800af app:id/drawer_layout}": {
                        "com.bluestacks.launcher.widget.ItemOptionView{1c263fe VFED..... .F....ID 0,0-1600,864 #7f0800dd app:id/item_option}": {
                            "androidx.constraintlayout.widget.ConstraintLayout{eb0275f V.E...... ......ID 0,0-1600,864}": {
                                "android.widget.LinearLayout{bd7a64f V.E...... .......D 196,631-1404,864 #7f0800a5 app:id/dock}": {
                                    "android.widget.FrameLayout{558d2e5 V.E...... .......D 0,27-1208,233 #7f0800bb app:id/frameLayout}": {
                                        "android.widget.FrameLayout{312586b V.E...... .......D 0,0-1208,206}": {
                                            "android.widget.LinearLayout{948b861 V.E...... .......D 62,-8-1146,182 #7f080048 app:id/allappsLinearLayout}": {
                                                "android.widget.LinearLayout{82a3f86 VFE...C.. .......D 66,0-225,190 #7f080050 app:id/appOneLinearLayout}": {
                                                    "android.widget.FrameLayout{fc1047 V.E...... ......ID 29,34-129,134 #7f080058 app:id/app_image_one}": {
                                                        "android.widget.ImageView{632c074 V.ED..... ......ID 74,3-97,26 #7f08011b app:id/popup_image_one}": 15
                                                    },
                                                    "android.widget.TextView{7f7799d V.ED..... ........ 0,142-159,190 #7f080060 app:id/app_name_one}": 16,
                                                },
                                                "android.widget.LinearLayout{7dace12 VFE...C.. .......D 225,0-384,190 #7f080053 app:id/appTwoLinearLayout}": {
                                                    "android.widget.FrameLayout{6df69e3 V.E...... ......ID 29,34-129,134 #7f08005b app:id/app_image_two}": {
                                                        "android.widget.ImageView{7f56fe0 I.ED..... ......ID 74,3-97,26 #7f08011e app:id/popup_image_two}": 19
                                                    },
                                                    "android.widget.TextView{2d71299 V.ED..... ........ 0,142-159,190 #7f080063 app:id/app_name_two}": 20,
                                                },
                                                "android.widget.LinearLayout{893b95e VFE...C.. .......D 384,0-543,190 #7f080052 app:id/appThreeLinearLayout}": {
                                                    "android.widget.FrameLayout{614c13f V.E...... ......ID 29,34-129,134 #7f08005a app:id/app_image_three}": {
                                                        "android.widget.ImageView{f71aa0c I.ED..... ......ID 74,3-97,26 #7f08011d app:id/popup_image_three}": 23
                                                    },
                                                    "android.widget.TextView{67d3f55 V.ED..... ........ 0,142-159,190 #7f080062 app:id/app_name_three}": 24,
                                                },
                                                "android.widget.LinearLayout{d5e0d6a VFE...C.. .......D 543,0-702,190 #7f08004f app:id/appFourLinearLayout}": {
                                                    "android.widget.FrameLayout{31e325b V.E...... ......ID 29,34-129,134 #7f080057 app:id/app_image_four}": {
                                                        "android.widget.ImageView{4955af8 V.ED..... ......ID 74,3-97,26 #7f08011a app:id/popup_image_four}": 27
                                                    },
                                                    "android.widget.TextView{91f7bd1 V.ED..... ........ 0,142-159,190 #7f08005f app:id/app_name_four}": 28,
                                                },
                                                "android.widget.LinearLayout{ec79636 VFE...C.. .......D 702,0-860,190 #7f08004e app:id/appFiveLinearLayout}": {
                                                    "android.widget.FrameLayout{e839937 V.E...... ......ID 29,34-129,134 #7f080056 app:id/app_image_five}": {
                                                        "android.widget.ImageView{e412ea4 I.ED..... ......ID 74,3-97,26 #7f080119 app:id/popup_image_five}": 31
                                                    },
                                                    "android.widget.TextView{4cf040d V.ED..... ........ 0,142-158,190 #7f08005e app:id/app_name_five}": 32,
                                                },
                                                "android.widget.LinearLayout{e6edfc2 VFE...C.. .......D 860,0-1018,190 #7f080051 app:id/appSixLinearLayout}": {
                                                    "android.widget.FrameLayout{f6e91d3 V.E...... ......ID 29,34-129,134 #7f080059 app:id/app_image_six}": {
                                                        "android.widget.ImageView{eb49110 V.ED..... ......ID 74,3-97,26 #7f08011c app:id/popup_image_six}": 35
                                                    },
                                                    "android.widget.TextView{974d409 V.ED..... ........ 0,142-158,190 #7f080061 app:id/app_name_six}": 36,
                                                },
                                            },
                                            "android.widget.ProgressBar{3826fc8 G.ED..... ......I. 589,88-619,118 #7f0800a6 app:id/dockLoadingBar}": 37,
                                        },
                                        "android.view.View{931c1ba V.ED..... ......ID 0,90-1208,206 #7f08017b app:id/viewBackground}": 38,
                                    },
                                    "android.widget.TextView{f9811dc V.ED..... ........ 0,9-1208,27 #7f080118 app:id/popular_gam}": 39,
                                },
                                "com.bluestacks.launcher.widget.GroupPopupView{74f360e IFE...C.. ......ID 0,0-1600,864 #7f0800c2 app:id/groupPopup}": {
                                    "androidx.cardview.widget.CardView{6a0c61c I.E...... ......ID 0,0-647,406}": {
                                        "android.widget.LinearLayout{c06782f V.E...... ......ID 6,6-641,400}": {
                                            "android.widget.TextView{ab9ae3c VFED..C.. ........ 25,20-635,54 #7f0800c4 app:id/group_popup_label}": 43,
                                            "com.bluestacks.launcher.widget.CellContainer{28da7c5 I.ED..... ......ID 37,54-598,374 #7f0800c1 app:id/group}": 44,
                                        }
                                    }
                                },
                                "com.bluestacks.launcher.widget.Desktop{75b098 VFED..... ......ID 44,166-1556,554 #7f08009c app:id/desktop}": {
                                    "com.bluestacks.launcher.widget.CellContainer{b7ab0f1 V.ED..... ......ID 0,0-1512,388}": {
                                        "d1.b{8cf4d6 VFED..CL. ........ 0,0-252,194}": 47,
                                        "d1.b{221a357 VFED..CL. ........ 252,0-504,194}": 48,
                                        "d1.b{4613e44 VFED..CL. ........ 504,0-756,194}": 49,
                                        "d1.b{af86b2d VFED..CL. ........ 756,0-1008,194}": 50,
                                        "d1.b{e3b8862 VFED..CL. ........ 1008,0-1260,194}": 51,
                                        "d1.b{25367c7 VFED..CL. ......I. 0,0-0,0}": 52,
                                    }
                                },
                                "android.widget.RelativeLayout{f79e5ac VFE...C.. ......ID 501,81-1100,130 #7f080133 app:id/searchRelativeLayout}": {
                                    "android.widget.ImageView{9e96275 V.ED..... ......ID 19,14-38,33 #7f080132 app:id/searchPlayIcon}": 54,
                                    "android.widget.ImageView{fdcc20a VFED..C.. ......ID 561,14-580,33 #7f080131 app:id/searchIcon}": 55,
                                    "android.widget.EditText{1d9da7b VFED..CL. ......ID 37,0-561,49 #7f080130 app:id/searchEditText}": 56,
                                },
                                "android.widget.LinearLayout{c55fab0 I.E...... ......ID 737,570-864,600 #7f0800d9 app:id/install_progress_layout}": {
                                    "android.widget.ProgressBar{71d8d29 V.ED..... ......ID 10,7-25,22 #7f0800ec app:id/loadingBar}": 58,
                                    "android.widget.TextView{f4dc8ae V.ED..... ......ID 35,4-117,25 #7f0800da app:id/installingGame}": 59,
                                },
                                "com.bluestacks.launcher.widget.PagerIndicator{b31df3 I.ED..... ......ID 0,554-1600,570 #7f08009d app:id/desktopIndicator}": 60,
                                "android.view.View{6cca51a V.ED..... ......ID 44,166-82,554 #7f0800e3 app:id/leftDragHandle}": 61,
                                "android.view.View{b8c684b V.ED..... ......ID 1518,166-1556,554 #7f080128 app:id/rightDragHandle}": 62,
                            },
                            "com.bluestacks.launcher.widget.ItemOptionView$c{7917228 V.ED..... ........ 0,0-1600,864}": 63,
                        }
                    }
                }
            },
            "android.view.ViewStub{d860eb2 G.E...... ......I. 0,0-0,0 #102018a android:id/action_mode_bar_stub}": 64,
        }
    }
}

data2 = """  
    MIME Typed Actions:
      com.android.camera.action.REVIEW:
        222a358 com.android.gallery3d/.app.GalleryActivity filter ca957c3
          Action: "android.intent.action.VIEW"
          Action: "com.android.camera.action.REVIEW"
          Category: "android.intent.category.DEFAULT"
          Category: "android.intent.category.BROWSABLE"
          Scheme: ""
          Scheme: "http"
          Scheme: "https"
          Scheme: "content"
          Scheme: "file"
          Type: "image"
          Type: "application/vnd.google.panorama360+jpg"
          mPriority=0, mOrder=0, mHasPartialTypes=true
        222a358 com.android.gallery3d/.app.GalleryActivity filter a9f840
          Action: "com.android.camera.action.REVIEW"
          Category: "android.intent.category.DEFAULT"
          Category: "android.intent.category.BROWSABLE"
          Scheme: "http"
          Scheme: "https"
          Scheme: "content"
          Scheme: "file"
          Type: "video/mpeg4"
          Type: "video/mp4"
          Type: "video/3gp"
          Type: "video/3gpp"
          Type: "video/3gpp2"
          Type: "application/sdp"
      androidx.activity.result.contract.action.PICK_IMAGES:
        2b8c15d com.google.android.gms/.photopicker.ui.PhotoPickerActivity filter b2e6b61
          Action: "androidx.activity.result.contract.action.PICK_IMAGES"
          Category: "android.intent.category.DEFAULT"
          Type: "image"
          Type: "video"
          mPriority=0, mOrder=0, mHasPartialTypes=true"""

conv2 = indent2dict(data2, removespaces=True)
print(conv2)

{
    "MIME Typed Actions:": {
        "com.android.camera.action.REVIEW:": {
            "222a358 com.android.gallery3d/.app.GalleryActivity filter ca957c3": {
                'Action: "android.intent.action.VIEW"': 5,
                'Action: "com.android.camera.action.REVIEW"': 6,
                'Category: "android.intent.category.DEFAULT"': 7,
                'Category: "android.intent.category.BROWSABLE"': 8,
                'Scheme: ""': 9,
                'Scheme: "http"': 10,
                'Scheme: "https"': 11,
                'Scheme: "content"': 12,
                'Scheme: "file"': 13,
                'Type: "image"': 14,
                'Type: "application/vnd.google.panorama360+jpg"': 15,
                "mPriority=0, mOrder=0, mHasPartialTypes=true": 16,
            },
            "222a358 com.android.gallery3d/.app.GalleryActivity filter a9f840": {
                'Action: "com.android.camera.action.REVIEW"': 18,
                'Category: "android.intent.category.DEFAULT"': 19,
                'Category: "android.intent.category.BROWSABLE"': 20,
                'Scheme: "http"': 21,
                'Scheme: "https"': 22,
                'Scheme: "content"': 23,
                'Scheme: "file"': 24,
                'Type: "video/mpeg4"': 25,
                'Type: "video/mp4"': 26,
                'Type: "video/3gp"': 27,
                'Type: "video/3gpp"': 28,
                'Type: "video/3gpp2"': 29,
                'Type: "application/sdp"': 30,
            },
        },
        "androidx.activity.result.contract.action.PICK_IMAGES:": {
            "2b8c15d com.google.android.gms/.photopicker.ui.PhotoPickerActivity filter b2e6b61": {
                'Action: "androidx.activity.result.contract.action.PICK_IMAGES"': 33,
                'Category: "android.intent.category.DEFAULT"': 34,
                'Type: "image"': 35,
                'Type: "video"': 36,
                "mPriority=0, mOrder=0, mHasPartialTypes=true": 37,
            }
        },
    }
}

```