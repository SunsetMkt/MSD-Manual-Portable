# MSD-Manual-Portable
A method to build a portable and offline-available MSD Manual.

一种构建便携式离线[《默沙东诊疗手册》](https://www.msdmanuals.cn/professional/)的方法。

在这里，我们以*默沙东诊疗手册（医学专业人士版）*为例。

## 关于《默沙东诊疗手册》
> 1899 年首次作为医生和药剂师的小型参考书出版，本手册的内容和范围日益增长，成为专业医护人员和消费者使用最广泛的综合性医学资源之一。 随着本手册的发展，它不断扩充内容的广度和深度以反映其使命，即向各界用户，包括医学从业人员和医学学生、兽医和兽医学生以及消费者，提供当下最好的医学信息。

[来源](https://www.msdmanuals.cn/professional/resourcespages/about-the-manuals)

## 启发
[默沙东诊疗手册（医学专业人士版）](https://play.google.com/store/apps/details?id=com.msd.professionalChinese)手机应用程序会在更新时请求`https://mmcdnprdcontent.azureedge.net/MSDZHProfessionalMedicalTopics.zip`，这使得完整获取手册内容成为可能。

（其亦有行为请求`https://mmcdnprdcontent.azureedge.net/MSDZHProfessionalImages.zip`，但根据验证，此文件内容已包含在前述请求中，不具备研究价值。）

请运行`getZip.py`获取并解压资源文件。

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
```

我们将整个手册的内容结构定义为`Section-Chapter-Topic`的结构，其中：
* sections.json 记录所有`Section`的信息
* TopicResources.json 作用尚未明确，引用的UUID不属于任何文件
* allchapterstopics.json 记录部分`Chapter-Topic`的信息，但`Section-Chapter`是明确的
* allcvtopicresources.json 作用尚未明确，可能与`临床计算器`功能有关

### `sections.json`内容举例
```json
{
    "sections": [
        {
            "SectionId": "{DE96F353-7424-424F-8C0E-9BB81B9C9BAF}",
            "Title": "临床药理学",
            "DisplayTitle": "临床药理学",
            "UniqueID": "v878847_zh",
            "LastUpdatedDate": "20220404T180617Z",
            "DisplayInMenu": true,
            "URLPathSegment": "clinical-pharmacology"
        },
        ...
```

### `TopicResources.json`内容举例
```json
[
    {
        "Title": "药物不良反应(ADRs)的分类",
        "SitecoreItemId": "{36a89baf-5697-489c-bedb-0a12274f7563}",
        "Type": "2",
        "BrightcoveVideoId": null,
        "TopicId": "{7C4DB1A1-8C4B-4E09-AB08-E28B8D0CFA3B}",
        "TopicName": "药物不良反应",
        "SectionName": "临床药理学"
    },
    ...
```

### `allchapterstopics.json`内容举例
```json
[
    {
        "Id": "{43035972-6114-459A-BD78-C9A953D36D8D}",
        "Name": "（DVT）深静脉血栓形成",
        "MetaInfo": "Topics",
        "SectionId": "{E14AE736-2EDB-4032-B362-805B1D86CEC2}",
        "SectionName": "心血管疾病",
        "TopicCount": null,
        "TopicId": null
    },
    ...
```

其中，`MetaInfo`字段为`Topics`或`Chapters`，`Id`字段对应资源文件目录中的同名HTML文件。

### `allcvtopicresources.json`内容举例
```json
[
    {
        "Title": "药物不良反应(ADRs)的分类",
        "SitecoreItemId": "{36a89baf-5697-489c-bedb-0a12274f7563}",
        "Type": "2",
        "BrightcoveVideoId": null,
        "TopicId": "{7C4DB1A1-8C4B-4E09-AB08-E28B8D0CFA3B}",
        "TopicName": "药物不良反应",
        "SectionName": "临床药理学"
    },
    ...
```

## JSON解析

### `Section-Chapter`
根据前述内容，通过`sections.json`和`allchapterstopics.json`我们可以完整获取`Section-Chapter`信息。

TODO

### `Section-Chapter-Topic`
TODO

## 搜索
通过分析`searchcontent.json`文件，我们可以获取到所有的搜索内容。

具体实现见`HTML/search.html`，将其置入`MSDZHProfessionalMedicalTopics`目录下即可。
