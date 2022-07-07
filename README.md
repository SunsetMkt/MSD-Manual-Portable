# MSD-Manual-Portable
A method to build a portable and offline-available MSD Manual.

一种构建便携式离线[《默沙东诊疗手册》](https://www.msdmanuals.cn/professional/)的方法。

在这里，我们以 *默沙东诊疗手册（医学专业人士版）* 为例。

## 关于《默沙东诊疗手册》
> 1899 年首次作为医生和药剂师的小型参考书出版，本手册的内容和范围日益增长，成为专业医护人员和消费者使用最广泛的综合性医学资源之一。 随着本手册的发展，它不断扩充内容的广度和深度以反映其使命，即向各界用户，包括医学从业人员和医学学生、兽医和兽医学生以及消费者，提供当下最好的医学信息。

[来源](https://www.msdmanuals.cn/professional/resourcespages/about-the-manuals)

## 启发
[默沙东诊疗手册（医学专业人士版）](https://play.google.com/store/apps/details?id=com.msd.professionalChinese)手机应用程序会在更新时请求`https://mmcdnprdcontent.azureedge.net/MSDZHProfessionalMedicalTopics.zip`，这使得完整获取手册内容成为可能。

（其亦有行为请求`https://mmcdnprdcontent.azureedge.net/MSDZHProfessionalImages.zip`，但根据验证，此文件内容已包含在前述请求中，不具备研究价值。）

请自行下载并解压缩`MSDZHProfessionalMedicalTopics.zip`至`MSDZHProfessionalMedicalTopics`目录。

## `MSDZHProfessionalMedicalTopics.zip`的文件结构
（仅保留对分析有价值的条目）
```tree
.
│  {000306F9-0E35-484C-8BBA-3BA56E6C7193}.html
│  【省略大量HTML文件】
│  {FFE89070-B96F-4616-83B4-F7FDFC6D041E}.html
│
├─Json
│      allchapterstopics.json
│      allcvtopicresources.json
│      appendixes.json
│      audio.json
│      calculators.json
│      equations.json
│      figures.json
│      images.json
│      labvalues.json
│      Pearls.json
│      searchcontent.json
│      sections.json
│      tables.json
│      threedmodels.json
│      TopicResources.json
│      video.json
│      {DE96F353-7424-424F-8C0E-9BB81B9C9BAF}.json
│      【省略部分JSON文件】
│      {C09D09EC-CB3A-4C21-8033-07DDBE02C814}.json
```

我们将整个手册的内容结构定义为`Section-Chapter-Topic`的结构，其中：
* `sections.json` 记录所有`Section`的信息，其中每个`Section`的UUID均对应`Json`中的一个文件。
* `TopicResources.json` 作用尚未明确，引用的UUID不属于任何文件
* `allchapterstopics.json` 作用尚未明确，记录部分`Chapter-Topic`的信息
* `allcvtopicresources.json` 作用尚未明确，可能与`临床计算器`功能有关
* `{Section的UUID}.json` 按照每个`Section`分别记录其中的`Chapter-Topic`信息

## JSON解析

### `Section-Chapter-Topic`
根据前述内容，通过`sections.json`和`{Section的UUID}.json`我们可以完整获取`Section-Chapter-Topic`对应信息。

### 搜索
通过分析`searchcontent.json`文件，我们可以获取到所有的搜索内容。

具体实现见`HTML/search.html`，将其置入`MSDZHProfessionalMedicalTopics`目录下即可。
