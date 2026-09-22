import Chat from './Chat'
import Sidebar from './Sidebar'

function Layout() {
  return (
    <div className="flex h-screen">
      <Sidebar />
      <Chat />
    </div>
  )
}

export default Layout


