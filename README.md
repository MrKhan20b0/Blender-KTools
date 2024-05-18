# Blender-KTools
Blender addon to make merging sub-meshes together for export quicker, and delete hidden vertices for optimization quicker.


<p align="center">
  <img src="/Imgs/KT_PANEL.png?raw=true" alt="S/Imgs/KT_PANEL.png?raw=true"/>
</p>


## Quickly delete vertices defined in delete-shapekeys
Shapkeys with "K_DELETE" in their name can be used to specify which vertices to delete frome a mesh. Any vertices moved in this shapekey will be deleted from the mesh.

This may be done destructivly, or done on duplicates

## Quickly merge meshes together based on name
Meshes contianing "_KM_Group" in their name, where "Group" is an alphnumeric string, will be merged together.

For example, "cube_KM_Pants_Long" & "sphere_KM__KM_Pants_Long" will be merged together and renamed to "Pants_Long"

This may be done destructivly, or done on duplicates

You may quickly change group names or assign group names using "Assign To Group".
All selected objects will change their group name to the user provided name.
