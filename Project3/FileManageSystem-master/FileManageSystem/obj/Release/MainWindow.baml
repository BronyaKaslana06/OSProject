   M S B A M L   `   `   `  ���� K  GFileManageSystem, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null3clr-namespace:FileManageSystemFileManageSystem  U QMaterialDesignThemes.Wpf, Version=2.3.0.823, Culture=neutral, PublicKeyToken=nulleHclr-namespace:MaterialDesignThemes.Wpf;assembly=MaterialDesignThemes.WpfMaterialDesignThemes.Wpf O Kmscorlib, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e0891&clr-namespace:System;assembly=mscorlibSystem 3clr-namespace:FileManageSystemFileManageSystem  !    FileManageSystem.MainWindow   'modeclr-namespace:FileManageSystem  W SPresentationCore, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35R NWindowsBase, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35\ XPresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35D 9http://schemas.microsoft.com/winfx/2006/xaml/presentation    R NSystem.Xaml, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089:x,http://schemas.microsoft.com/winfx/2006/xaml     @d2http://schemas.microsoft.com/expression/blend/2008     Jmc;http://schemas.openxmlformats.org/markup-compatibility/2006     XwpfHclr-namespace:MaterialDesignThemes.Wpf;assembly=MaterialDesignThemes.Wpf     9system&clr-namespace:System;assembly=mscorlib     0localclr-namespace:FileManageSystem     FmaterialDesign1http://materialdesigninxaml.net/winfx/xaml/themes     MaterialDesignBody#���   $��Regular"�$��13(�&   System.Windows.Media.TextOptions    TextFormattingMode$  Ideal=�   TextRenderingMode$
 Auto=�  MaterialDesignPaper#���    MaterialDesignFont#���   � Title$* $1552730 寸宣堂 文件管理系统��$	��600��$
��1000�� � WindowStartupLocation$ CenterScreen=� � 	Resources    FileManageSystem.IsFolder  IsFolder��%   &	         .��)  #MaterialDesignThemes.Wpf.DialogHost  -   $��dialog_about��$��Right=�   CloseOnClickAway . .���  � RowDefinitions �� $��80 ��� $��30 ��� $��* ��� $��16 �.+�� $��0��.+�(  "MaterialDesignThemes.Wpf.ColorZone     Mode$ Light=�$��2,2,2,0q�$��1q�   CornerRadius$ 1��	 K� ZIndex$	 1��+  %MaterialDesignThemes.Wpf.ShadowAssist
   ShadowDepth$
 Depth1=�.���  � ColumnDefinitions �� $
��auto ��� $
��auto ��� $
��auto ��� $
��auto ��� $
��auto ��� $
��auto ��� $
��auto ��� $
��auto ��� $
��auto ��� $
��auto ��� $
��auto ��� $
��auto ��� $
��auto ��� $
��auto �.+��� -   $
��open��  MaterialDesignFlatButton#��[ $��0��$��80�� � ToolTip$ OpenFile��.����  �� Orientation$ Vertical=�.+�'  !MaterialDesignThemes.Wpf.PackIcon  �  �ControlzEx.PackIconBase`1[[MaterialDesignThemes.Wpf.PackIconKind, MaterialDesignThemes.Wpf, Version=2.3.0.823, Culture=neutral, PublicKeyToken=null]]   Kind$ 	OpenInNew=� J� Opacity$ 1Q�$��48��$��48���� $��打开��$��黑体)�$��Bottom=�$��CharacterEllipsis=�$��Center=�$��17���� -   $��
new_folder��#��[ $��1��$��80��$ Folder��.���� $ Vertical=�.+�  $ Folder=�$ 1Q�$��48��$��48���� $��新建文件夹��$��黑体)�$��Bottom=�$��CharacterEllipsis=�$��Center=�$��17���� -   $��new_file��#��[ $��2��$��80��$
 File��.���� $ Vertical=�.+�  $
 File=�$ 1Q�$��48��$��48���� $��新建文件��$��黑体)�$��Bottom=�$��CharacterEllipsis=�$��Center=�$��17���� -   $��rename��#��[ $��3��$��80��$ Rename��.���� $ Vertical=�.+�  $ 	RenameBox=�$ 1Q�$��48��$��48���� $��	重命名��$��黑体)�$��Bottom=�$��CharacterEllipsis=�$��Center=�$��17���� $��4��$	��0.5��
���   �$��	15,0,15,0q��� -   $
��copy��#��[ $��5��$��80��$
 Copy��.���� $ Vertical=�.+�  $ ContentCopy=�$ 1Q�$��48��$��48���� $��复制��$��黑体)�$��Bottom=�$��CharacterEllipsis=�$��Center=�$��17���� -   $��stick��#��[ $��6��$��80��$ Paste��.���� $ Vertical=�.+�  $ ContentPaste=�$ 1Q�$��48��$��48���� $��粘贴��$��黑体)�$��Bottom=�$��CharacterEllipsis=�$��Center=�$��17���� -   $	��cut��#��[ $��7��$��80��$	 Cut��.���� $ Vertical=�.+�  $ 
ContentCut=�$ 1Q�$��48��$��48���� $��剪切��$��黑体)�$��Bottom=�$��CharacterEllipsis=�$��Center=�$��17���� -	   $��delete��#��[ $��8��$��80��$ Details��.���� $ Vertical=�.+�  $ Close=�$ 1Q�$��48��$��48���� $��删除��$��黑体)�$��Bottom=�$��CharacterEllipsis=�$��Center=�$��17���� -
   #��[ $��9��$��80��$ Details��.���� $ Vertical=�.+�  $ Details=�$ 1Q�$��48��$��48���� $��属性��$��黑体)�$��Bottom=�$��CharacterEllipsis=�$��Center=�$��17���� $��10��$	��0.5��
���   �$��	15,0,15,0q��� -   #��[ $��11��$��80��$ Delete��.���� $ Vertical=�.+�  $ DeleteSweep=�$ 1Q�$��48��$��48���� $��	格式化��$��黑体)�$��Bottom=�$��CharacterEllipsis=�$��Center=�$��17���� #��[ $��12��$��80��$
 Help��.���� $ Vertical=�.+�  $
 Help=�$ 1Q�$��48��$��48���� $��帮助��$��黑体)�$��Bottom=�$��CharacterEllipsis=�$��Center=�$��17��� $��1�� �� $
��Auto ��� $
��105* ��� $��0* ��� $
��646* ��� $
��Auto �.+�� $��90��$��0�� �� $��* ��� $��* ��� $��* �.+�]� 
������ $��0��.+��� -     MaterialDesignToolButton#���  $��Center=�$	��Top=�.��  $ 	ArrowLeft=�$ 1Q�$��20��$��20��]� 
������ $��1��.+��� -   #���  $��Center=�$	��Top=�.��  $ 
ArrowRight=�$ 1Q�$��20��$��20��]� 
������ $��2��.+��� -   #���  $��Center=�$	��Top=�.��  $ ArrowUp=�$ 1Q�$��20��$��20��  $ Standard=�$��2q�$ 2��$	 1��$��1��$��1,1,1.333,0q�$
 Depth0=�$��3��.���  �� $��* ��� $��30 �.+��� -   $��pathView��$��0��$��5,0,0,0q�$��宋体)�.  (MaterialDesignThemes.Wpf.TextFieldAssist   DecorationVisibility$ Hidden=�$	��0.2q�$��Center=�$��2���� #���  $��2��$��Center=�.��  $ Refresh=�$ 1Q�  $��4��$	��150��$ Standard=�$��2q�$ 2��$	 1��$��0.667,1,1.333,0q�$
 Depth0=�.���  �� $��* ��� $��30 �.+��� -   $��search��$��0��$��0q�$��5,0,0,0q�)	  #MaterialDesignThemes.Wpf.HintAssist 	  Hint$ 搜索��$ Hidden=�$	��0.2q�$��2��$��Center=��� -   #���  $��1��$��Center=�.��  $ Magnify=�$ 1Q�]� $��2��.+��� -   $��scrollViewCategory��$
��Left=�$	��180��.��� .+�R� -   $��treeView��$
��Left=����� .R��� ����  �� DataType
   FileManageSystem.File" 
  �� ItemsSource �� *
SubFiles+.R��� $ 
Horizontal=�.+�  $��15��$��15�� �� *Type+�� ���� *Name+�� -   $��
scrollView��.��� .+�� $��10,0,0,0q� �� $	��150 ��� $	��2.4 ��� $	��200 ��� $	��2.4 ��� $	��100 ��� $	��2.4 ��� $	��100 �.+��� $
��Name��$��0��$��18(��� 
�������$��1��$	��0.4��$��0,0,2,0q�$��20��$	��Top=��� $
��Date��$��2��$��18(��� 
�������$��3��$	��0.4��$��0,0,2,0q�$��20��$	��Top=��� $
��Type��$��4��$��18(��� 
�������$��5��$	��0.4��$��0,0,2,0q�$��20��$	��Top=��� $
��Size��$��6��$��18(��� -    ��Name$ listBox��$��0,20,0,0q�$
��auto��$	��Top=�$
��Left=����� .R��� ���� .R��  �� $��15 ��� $	��140 ��� $	��200 ��� $	��100 ��� $	��100 � �� $��14 �.+�  $��0��$��0��$��15��$��15�� �� *Type+�� -   $��0��$��1��$��2,0,0,0q����� *Name+�� -   $��0��$��2������ *Date+�� -   $��0��$��3������ *Type+�� -   $��0��$��4������ *Size+ �� StringFormat$ {0} B��]� $��3��.+��� ._�]� .+��� $
��Left=� " MaterialDesignCaptionTextBlock#��[ 
1个对象�� -   $��bottom_space�� " PrimaryHueLightForegroundBrush#���  $��Right=�$��Right=�