import streamlit as st
from data.validator import validar_usuario
from data.loader import cargar_datos

# Importar vistas
from views.ranking_docentes_modulos import mostrar_ranking_por_plantel
import views.no_competentes as vista_nc
import views.comportamiento as vista_com
import views.modulos_criticos as vista_mc
import views.mostrar_estatal as vista_estatal
import views.bitacora_conexiones as vista_bc

st.set_page_config(page_title="Tablero Docente", layout="wide")

st.markdown("""
    <style>
    /* Oculta solo los íconos individuales dentro del toolbar */
    [data-testid="stToolbar"] > div:nth-child(n+2) {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# Inicializar sesión
# ----------------------------
if "logueado" not in st.session_state:
    st.session_state.update({
        "logueado": False,
        "plantel_usuario": None,
        "administrador": False
    })

# ----------------------------
# Login con imagen 
# ----------------------------
if not st.session_state.logueado:
    col1, col2 = st.columns([1, 2])

    with col1:
        st.title("🔐 Inicio de sesión")
        usuario = st.text_input("Usuario")
        contrasena = st.text_input("Contraseña", type="password")

        if st.button("Iniciar sesión"):
            ok, plantel, es_admin = validar_usuario(usuario, contrasena)
            if ok:
                st.session_state.update({
                    "logueado": True,
                    "plantel_usuario": plantel,
                    "administrador": es_admin
                })
                st.success("✅ ¡Sesión iniciada!")
                st.rerun()
            else:
                st.error("❌ Autenticación Incorrecta")

    with col2:
        try:
            st.image("utils/ImagenDashDocentes.png", use_container_width=True)
        except Exception:
            st.warning("⚠️ IMAGEN NO DISPONIBLE.")

    st.stop()

# ----------------------------
# Cierre de sesión
# ----------------------------
st.sidebar.success("✅ Sesión activa")
st.sidebar.info(f"👤 {'Administrador' if st.session_state.administrador else f'Plantel: {st.session_state.plantel_usuario}'})")

if st.sidebar.button("Cerrar sesión"):
    for key in ["logueado", "plantel_usuario", "administrador"]:
        st.session_state.pop(key, None)
    st.rerun()

# ----------------------------
# Cargar datos
# ----------------------------
df, error = cargar_datos()
if error:
    st.error(f"❌ Error,no se pueden cargar los datos: {error}")
    st.stop()

# ----------------------------
# Menú desplegable
# ----------------------------
if st.session_state.administrador:
    opciones = [
        "Docentes y Módulos",
        "Docentes Seguimiento",
        "Módulos Seguimiento",
        "Estatal Docentes y Módulos",
        "Bitácora de Conexiones"
    ]
else:
    opciones = [
        "Docentes y Módulos",
        "Docentes Seguimiento",
        "Módulos Seguimiento",
        "Ranking por docentes y módulos"
    ]

opcion = st.sidebar.selectbox("Menú Principal", opciones)

# ----------------------------
# VISTAS DISPONIBLES
# ----------------------------
if opcion == "Docentes y Módulos":
    vista_nc.mostrar(df, st.session_state.plantel_usuario, st.session_state.administrador)

elif opcion == "Estatal Docentes y Módulos" and st.session_state.administrador:
    vista_estatal.mostrar_estatal(df)

elif opcion == "Docentes Seguimiento":
    vista_com.mostrar(df, st.session_state.plantel_usuario, st.session_state.administrador)

elif opcion == "Módulos Seguimiento":
    vista_mc.mostrar(df, st.session_state.plantel_usuario, st.session_state.administrador)

elif opcion == "Bitácora de Conexiones" and st.session_state.administrador:
    vista_bc.mostrar()

elif opcion == "Ranking por docentes y módulos":
    mostrar_ranking_por_plantel(df, st.session_state.plantel_usuario)
