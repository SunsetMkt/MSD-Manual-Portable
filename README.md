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

具体实现见`HTML/menu.html`，将其置入`MSDZHProfessionalMedicalTopics`目录下即可。

### 搜索
通过分析`searchcontent.json`文件，我们可以获取到所有的搜索内容。

具体实现见`HTML/search.html`，将其置入`MSDZHProfessionalMedicalTopics`目录下即可。

## 快速开始
下载并解压缩`MSDZHProfessionalMedicalTopics.zip`至`MSDZHProfessionalMedicalTopics`目录，将`HTML`文件夹中文件全部置入`MSDZHProfessionalMedicalTopics`目录，在`MSDZHProfessionalMedicalTopics`目录启动HTTP服务器，即可访问手册。

这些步骤可以通过运行`start.py`自动完成。

## 版权声明
《默沙东诊疗手册》的版权归默沙东所有。

任何不当使用本项目导致的版权纠纷，项目作者均不承担任何责任。

请不要将生成内容用于商业用途。

《默沙东诊疗手册》内容仅供专业人士参考。

## 医疗内容免责声明 
本项目旨在为医药专业人员提供《默沙东诊疗手册》离线阅读服务，如果您不是医药专业人员，建议您不要使用此项目。如您并非医药专业人员，不论您基于任何原因使用此项目，您同意均不应参考《默沙东诊疗手册》内容作为诊断、治疗、预防、康复、使用医疗产品或其他任何产品的建议或意见，对此您应寻求执业医师及其他具备相应资质的专业人士意见并遵照医嘱。《默沙东诊疗手册》所载信息绝无意代替您自己的医学判断并且《默沙东诊疗手册》刊载的任何观点、评论和其他内容亦无意作为可以信赖的建议，因此，我们郑重声明因任何《默沙东诊疗手册》访问者或任何获知《默沙东诊疗手册》内容者基于对《默沙东诊疗手册》材料的信赖所引起的任何责任与义务都与《默沙东诊疗手册》无关。您同意默沙东和项目作者将不对您使用和/或依赖本网站内容、产品、信息或者资讯导致的直接或间接损失承担任何责任，并不对《默沙东诊疗手册》内容及其引述的产品、方法、资讯或其他材料的准确性、时效性、可适用性承担任何明示或暗示的保证责任。
