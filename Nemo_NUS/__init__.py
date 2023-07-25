bl_info = {
        'name'			: 'Finding Nemo NUS Level NuNus',
	'author'		: 'DarkShadow Nemo',
	'version'		: (0, 0, 1),
	'blender'		: (3, 0, 0),
	'location'		: 'File > Import-Export',
	'description'           : 'Import NUS and export from the gamecube of finding nemo',
	'category'		: 'Chunk-Importer and Chunk-Exporter'
}
import os
import bpy
import importlib
from bpy.props import CollectionProperty, StringProperty, BoolProperty, EnumProperty, FloatProperty, IntProperty
from bpy_extras.io_utils import ImportHelper, ExportHelper


from.import nuNus_import

class ImportnuNus(bpy.types.Operator, ImportHelper):
        bl_idname  = 'import_nunus.nus'
        bl_label   = 'Import NuNus NUS'
        bl_options = {'UNDO'}
        filename_ext = '.nus'
        files: CollectionProperty(
                name	    = 'File path',
                description = 'File path used for finding the NUS Nemo GameCube file level.',
                type	    = bpy.types.OperatorFileListElement
        )
        directory: StringProperty()
        filter_glob: StringProperty(default = '*.nus', options = {'HIDDEN'})
        def execute(self, context):
                paths = [os.path.join(self.directory, name.name) for name in self.files]
                if not paths: paths.append(self.filepath)
                importlib.reload(nuNus_import)
                for path in paths: nuNus_import.NUSRead(path)
                return {'FINISHED'}

class ExportnuNus(bpy.types.Operator, ExportHelper):
        bl_idname  = 'export_nunus.nus'
        bl_label   = 'Export NuNus NUS'
        bl_options = {'UNDO'}
        filename_ext = '.nus'
        files: CollectionProperty(
                name	    = 'File path',
                description = 'File path used for finding the NUS Nemo GameCube file level',
                type	    = bpy.types.OperatorFileListElement
        )

        directory: StringProperty()
        filter_glob: StringProperty(default = '*.nus', options = {'HIDDEN'})

        def execute(self, context):
            importlib.reload(nuNus_import)
            nuNus_import.NUSWrite(self.filepath)
            return {"FINISHED"}
        


	
def menu_func_import(self, context):
        self.layout.operator(ImportnuNus.bl_idname, text='nuNus Importer (.nus)')

def menu_func_export(self, context):
        self.layout.operator(ExportnuNus.bl_idname, text='nuNus Exporter (.nus)')

def register():
        bpy.utils.register_class(ImportnuNus)
        bpy.utils.register_class(ExportnuNus)
        bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
        bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
def unregister():
        bpy.utils.unregister_class(ImportnuNus)
        bpy.utils.unregister_class(ExportnuNus)
        bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
        bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
if __name__ == '__main__':
        register()
