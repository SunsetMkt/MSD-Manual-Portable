# MSD-Manual-Portable
A method to build a portable and offline-available MSD Manual.

一种构建便携式离线[《默沙东诊疗手册》](https://www.msdmanuals.cn/professional/)的方法。

在这里，我们以 *默沙东诊疗手册（医学专业人士版）* 为例。

## Quick Start
```shell
$ pip3 install -r requirements.txt
$ python3 MSD-Manual-Portable.py
```

## usage
```shell
usage: MSD-Manual-Portable.py [-h] [-l {en,zh}] [-v {professional,consumer}] [-p PORT] [-s]

Host a portable and offline-available MSD Manual.

options:
  -h, --help            show this help message and exit
  -l {en,zh}, --lang {en,zh}
                        Language of the MSD Manual. Default: zh
  -v {professional,consumer}, --version {professional,consumer}
                        Version of the MSD Manual. Default: professional
  -p PORT, --port PORT  Port of the HTTP Server. Default port changes for different languages and versions.
  -s, --silent          Do not open browser.
```

## 关于《默沙东诊疗手册》
> 1899 年首次作为医生和药剂师的小型参考书出版，《默沙东诊疗手册》的内容和范围日益增长，成为专业医护人员和消费者使用最广泛的综合性医学资源之一。 随着《默沙东诊疗手册》的发展，它不断扩充内容的广度和深度以反映其使命，即向各界用户，包括医学从业人员和医学学生、兽医和兽医学生以及消费者，提供当下最好的医学信息。

[来源](https://www.msdmanuals.cn/professional/resourcespages/about-the-manuals)

## 启发
[默沙东诊疗手册（医学专业人士版）](https://play.google.com/store/apps/details?id=com.msd.professionalChinese)手机应用程序会在更新时请求`https://mmcdnprdcontent.azureedge.net/MSDZHProfessionalMedicalTopics.zip`，这使得完整获取手册内容成为可能。

（其亦有行为请求`https://mmcdnprdcontent.azureedge.net/MSDZHProfessionalImages.zip`，但根据验证，此文件内容已包含在前述请求中，不具备研究价值。）

请自行下载并解压缩`MSDZHProfessionalMedicalTopics.zip`至`MSDZHProfessionalMedicalTopics`目录。

在文档撰写时，文件校验和信息如下：

```
名称: MSDZHProfessionalMedicalTopics.zip
大小: 163803563 字节 (156 MiB)
CRC32: C97C55A5
CRC64: 15D20E4F37A0B579
SHA256: 2b0662f46a65c54381f0998247ef7f6a592322e82457352876da869b7c7920c5
SHA1: eb8333c36fa09b95b4da2388ef6564d0f1096de8
BLAKE2sp: d0de7b61c3b50721c5afead245077153a3559f36f152d8148b9f7fe278b5912d
```

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

这些步骤可以通过运行`MSD-Manual-Portable.py`自动完成，在第一次成功启动后不再需要互联网连接。

无需理会浏览器控制台提示错误和HTTP服务器显示的任何404错误，这些错误由手册资源文件自身造成且不会影响手册的正常显示。

（由于手册资源文件和目录/搜索功能构建的特殊性，HTTP服务器是必须的，否则相应功能将无法使用。）

## 获取其他语言的资源文件
令人遗憾的是，《默沙东诊疗手册》的中文译本内容在更新进度上远不及英语版本，其他语言版本亦存在类似的问题。

对于英文版本的资源文件，其URL为`https://mmcdnprdcontent.azureedge.net/MSDProfessionalMedicalTopics.zip`。

在文档撰写时，文件校验和信息如下：

```
名称: MSDProfessionalMedicalTopics.zip
大小: 201545636 字节 (192 MiB)
CRC32: 5C2FDCE2
CRC64: 5D9A6E88EB6E2767
SHA256: 0e1817e579e4c7a4a1df3fe93e2e137f6c523d437afdccc29a3feac54f8c9f7e
SHA1: 3696f1f82d88a62cda2208b4057fb58d7c9d4252
BLAKE2sp: 5e76aaecb491188c4be6baa719293b7b1d4b8ac832c1763189e15249d16f26fc
```

若需要获取其他语言版本的资源文件，请自行获取URL并解压缩。

`python3 MSD-Manual-Portable.py -l en`适用于获取英文版本资源文件。如若在同一个浏览器中启动过其他语言版本，则可能需要在目录(Menu)/搜索(Search)页面选择`Refresh`以便清除为了便于加载而在浏览器中本地存储的上个语言版本的缓存信息。

## 版权声明
《默沙东诊疗手册》的版权归默沙东所有。此项目与默沙东无关。

任何不当使用本项目导致的版权纠纷，项目作者均不承担任何责任。

请不要将生成内容用于商业用途。

## 免责声明
此项目仅用于学习和技术交流，不保证其准确性、完整性、可靠性，请用户自行根据实际情况自行判断使用。

## 医疗内容免责声明 
本项目旨在为医药专业人员提供《默沙东诊疗手册》离线阅读服务，如果您不是医药专业人员，建议您不要使用此项目。如您并非医药专业人员，不论您基于任何原因使用此项目，您同意均不应参考《默沙东诊疗手册》内容作为诊断、治疗、预防、康复、使用医疗产品或其他任何产品的建议或意见，对此您应寻求执业医师及其他具备相应资质的专业人士意见并遵照医嘱。《默沙东诊疗手册》所载信息绝无意代替您自己的医学判断并且《默沙东诊疗手册》刊载的任何观点、评论和其他内容亦无意作为可以信赖的建议，因此，我们郑重声明因任何《默沙东诊疗手册》访问者或任何获知《默沙东诊疗手册》内容者基于对《默沙东诊疗手册》材料的信赖所引起的任何责任与义务都与《默沙东诊疗手册》无关。您同意默沙东和项目作者将不对您使用和/或依赖《默沙东诊疗手册》内容、产品、信息或者资讯导致的直接或间接损失承担任何责任，并不对《默沙东诊疗手册》内容及其引述的产品、方法、资讯或其他材料的准确性、时效性、可适用性承担任何明示或暗示的保证责任。

《默沙东诊疗手册》的作者、审校者和编辑已付出巨大努力确保治疗、药物和给药方案准确并符合在出版时可接受的标准。然而，由于科学研究和临床实践的不断发展与充实，医学知识日益更新，权威专家的见解可能存在差异，个体临床病情的独特性，加之本材料在编写过程中难免出现人为的错误，所以《默沙东诊疗手册》上的信息可能会与其他来源的医学信息存在差异。《默沙东诊疗手册》上的信息并非旨在提供专业意见，也不能代替由有资质的医生、药剂师或其他医疗保健专业人员所提供的当面咨询。读者不能因为《默沙东诊疗手册》上提供的某些信息，而无视医生的建议或延迟就医。

《默沙东诊疗手册》中的内容体现的是美国的医疗操作和信息。其他国家的临床指南、操作规范和专业意见可能有别，因此建议读者也要咨询当地的医疗资源。请注意，并非英文书写的所有内容，都在各种语言的翻译版本中可以找到。
