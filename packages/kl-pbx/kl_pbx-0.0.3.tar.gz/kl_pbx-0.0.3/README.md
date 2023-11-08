# pbx

pip install -r kl_pbx

# use

import lib

```

from kl_pbx import PBXProjectHelper,PBXTreeType,PBXGetSetfrom

```

init project

```
main_target="UnityFramework"
 projectpath = os.path.join(self.work_project_path, "Unity-iPhone.xcodeproj/project.pbxproj")
  pbx_helpr = PBXProjectHelper(projectpath)

```

add group

```
mygroup = pbx_helpr.add_group("ios", "")
```

add a system lib to group

```
pbx_helpr.add_file(main_target, "user/lib/libz.1.2.5.tbd", mygroup, PBXTreeType.SDKROOT)
```

add a system framwork to group

```
frameworkgroup = pbx_helpr.add_group("Frameworks", "", mygroup)
 pbx_helpr.add_file(main_target, "System/Library/Frameworks/AudioToolbox.framework", frameworkgroup, PBXTreeType.SDKROOT, PBXGetSet(attribs))
```

add files to group
filepath is full path of disk

```
 pbx_helpr.add_file(main_target, filepath, mygroup, PBXTreeType.SOURCE_ROOT)
```

add folders to group
folder is full path of disk

```
pbx_helpr.add_folder(main_target, folderpath, mygroup, excludes=self.ios_build_config.excludes)
```

add flags

```
pbx_helpr.add_flags(main_target, "OTHER_LDFLAGS", ["-ObjC", "-lz", "-lstdc++"])
```

change flags

```
pbx_helpr.set_flags(main_target, 'IPHONEOS_DEPLOYMENT_TARGET', "11.0")
```

change code sign

```
pbx_helpr.change_code_sign("Unity-iPhone","Apple Development: Chongyu Lu (F3Q2Q5F68Y)","hoc_jpsgp_dev")
```

change package name

```
pbx_helpr.change_package_name("Unity-iPhone", "com.package,kl")
```

save all change

```
pbx_helpr.save()
```
