   M S B A M L   `   `   `  ���� K  GFileManageSystem, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null3clr-namespace:FileManageSystemFileManageSystem  #    FileManageSystem.DetailWindow   W SPresentationCore, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35R NWindowsBase, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35\ XPresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35D 9http://schemas.microsoft.com/winfx/2006/xaml/presentation    R NSystem.Xaml, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089:x,http://schemas.microsoft.com/winfx/2006/xaml     @d2http://schemas.microsoft.com/expression/blend/2008     Jmc;http://schemas.openxmlformats.org/markup-compatibility/2006     U QMaterialDesignThemes.Wpf, Version=2.3.0.823, Culture=neutral, PublicKeyToken=nullFmaterialDesign1http://materialdesigninxaml.net/winfx/xaml/themes  *localclr-namespace:FileManageSystem    � Title$  DetailWindow��$	��350��$	��280�� � WindowStartupLocation$ CenterScreen=� � Topmost . .���  � RowDefinitions �� $
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
��auto �.+�� $��0�� � ColumnDefinitions �� $��70 ��� $��* �.+�'  !MaterialDesignThemes.Wpf.PackIcon  �  �ControlzEx.PackIconBase`1[[MaterialDesignThemes.Wpf.PackIconKind, MaterialDesignThemes.Wpf, Version=2.3.0.823, Culture=neutral, PublicKeyToken=null]]   Kind$
 File=� J� Opacity$ 1Q�$��60��$��60��$��0���� -   $��detains_name��$��1��$��3,0,0,0q�$��0,0,50,0q�$��DB��.  (MaterialDesignThemes.Wpf.TextFieldAssist   DecorationVisibility$ Hidden=�$	��0.5q�$��Center=�$��2���� $��1��$��1��
�������$��8q�� $��2�� �� $��70 ��� $��* �.+��� $��文件类型: ��$��0��$��Center=�$��9q��� -   $��detains_type��$
��File��$��1��$��Center=�$��9q��� $��1��$��1��
�������$��8q�� $��3�� �� $��70 ��� $��* �.+��� $��文件大小: ��$��0��$��Center=�$��9,0,0,0q��� -   $��detains_size��$��1200 B��$��1��$��Center=�$��9,0,0,0q�� $��4�� �� $��70 ��� $��* �.+��� $��占用大小: ��$��0��$��Center=�$��9,0,0,0q��� -   $��detains_op_size��$��1524 B��$��1��$��Center=�$��9,0,0,0q��� $��5��$��1��
�������$��8q�� $��6�� �� $��70 ��� $��* �.+��� $��文件位置: ��$��0��$��Center=�$��9,0,0,0q��� -   $��detains_path��$��CxtDisk/OS/Homework��$��1��$��Center=�$��9,0,0,0q��� $��7��$��1��
�������$��8q�� $��8�� �� $��70 ��� $��* �.+��� $��修改时间: ��$��0��$��Center=�$��9,0,0,0q��� -   $��detains_date��$��2000-10-13 12:10:10��$��1��$��Center=�$��9,0,0,0q��� $��9��$��1��
�������$��8q�� $��10�� �� $��70 ��� $��* ��� $��* �.+��� $��	属性 : ��$��0��$��Center=�$��9,0,0,0q��� -   $��detains_is_read��$��只读��$��1��$��Center=�$��9,0,0,0q��� -   $��detains_is_write��$��读写��$��2��$��Center=�$��0,0,0,0q�