import useStore from "../state/counterStore"


function App() {
  const count = useStore((state) => state.count)
  const increment = useStore((state) => state.increment)
  const decrement = useStore((state) => state.decrement)
  const reset = useStore((state) => state.reset)

  return (
    <>
      <h1>Current count: {count}</h1>
      <button onClick={increment}>Increment</button>
      <button onClick={decrement}>Decrement</button>
      <button onClick={reset}>Reset</button>
    </>
  )
}

export default App


