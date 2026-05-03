# Proposal: Corregir bug trigger registro — columna email inexistente

## Intent

El trigger `handle_new_user()` en `supabase_schema.sql` falla al intentar insertar en una columna `email` que no existe en la tabla `profiles`. Esto causa el error "An error occurred" durante el registro de nuevos usuarios.

## Scope

### In Scope
- Eliminar referencia a columna `email` inexistente en el trigger `handle_new_user()`
- Verificar que el resto del trigger funcione correctamente con los campos existentes

### Out of Scope
- Agregar columna `email` a la tabla `profiles` (decisión de diseño futura)
- Modificar el flujo de autenticación de Supabase

## Capabilities

### Modified Capabilities
- `user-registration`: El flujo de registro actualmente falla por referencia a columna inexistente

## Approach

Eliminar `email` del `INSERT` del trigger, quedando:

```sql
INSERT INTO public.profiles (id, full_name)
VALUES (NEW.id, NEW.raw_user_meta_data->>'full_name');
```

El `email` del usuario ya está disponible en `auth.users` via `NEW.email`, pero no necesita persistirse en `profiles` si no existe la columna.

## Affected Areas

| Area | Impact | Description |
|------|--------|-------------|
| `backend/supabase_schema.sql` | Modified | Trigger `handle_new_user()` —移除 columna `email` del INSERT |

## Risks

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Ninguno — cambio minimal y focalizado | Low | Solo se elimina código roto; si `email` se necesitara en el futuro, se agrega la columna primero |

## Rollback Plan

Revertir el cambio editando el trigger para volver a incluir `email` en el INSERT. La función `public.handle_new_user()` se redefine completamente, así que es un replace directo.

## Dependencies

- Ninguna — es un cambio atómico en un solo archivo SQL

## Success Criteria

- [ ] El trigger `handle_new_user()` compila sin errores en Supabase
- [ ] El registro de nuevos usuarios no produce errores
- [ ] El perfil se crea correctamente con `id` y `full_name`