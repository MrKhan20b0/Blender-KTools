# Blender-KTools (WIP)
Blender addon to make merging sub-meshes together for export quicker, and delete hidden vertices for optimization quicker.


## Quickly delete vertices defined in delete-shapekeys
Shapkeys with "DELETE" in their name can be used to specify which vertices to delete frome a mesh. Any vertices moved in this shapekey will be deleted from the mesh.

This may be done destructivly, or done on duplicates

## Quickly merge meshes together based on name
Meshes contianing "__MERGE_X", where X is a alphnumeric character, will be merged together.

For example, cube__MERGE_A & sphere__MERGE_A will be merged together.

This may be done destructivly, or done on duplicates
