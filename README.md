# AutoShaderScript_MayaEdu
This script is for artists who personally use Maya like Education or Indie version with V-Ray and Substance Painter. It will help you many setup of shaders automatically.
> 이 스크립트는 V-Ray와 서브스턴스 페인터와 함께 마야 교육용 이나 인디버전을 개인적으로 사용하는 아티스트를 위한 것입니다. 스크립트는 여러분에게 자동으로 많은 셰이더 셋업을 도와줄 것입니다.

## Installation
1. Put two scripts(ShaderMain.py, ShaderSetup.py) into a Maya scripts directory.
> 2개의 스크립트(ShaderMain.py, ShaderSetup.py)를 마야 스크립트 디렉토리에 넣어주세요.
* Windows: C:\Users\{user_directory}\Documents\maya\scripts
2. Write these commands on Script Editor or Shelf Editor of Maya.
> 마야의 스크립트 에디터와 셸프 에디터에 이 명령어들을 작성해주세요.
	import ShaderMain
	reload(ShaderMain)
	ShaderMain.MainWindow()