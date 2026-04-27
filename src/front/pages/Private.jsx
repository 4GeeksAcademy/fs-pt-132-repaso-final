import { useEffect } from "react"
import { useNavigate } from "react-router-dom"

const Private = () => {
    const navigate = useNavigate()
    useEffect(()=>{
        if (!localStorage.getItem('token')) navigate('/')
    },[])




return(
    <div>
        private page


    </div>
)

}


export default Private