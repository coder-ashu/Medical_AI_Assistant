export const Loading = () => {
  return (
    <div className="h-screen w-full flex flex-col justify-center items-center bg-black">
      <img
        src="/logo.svg"
        alt="Logo"
        className="w-8 h-48 animate-pulse"
      />
    </div>
  )
}
