interface StartConversationProps {
  onSubmit: () => void;
}

const StartConversation: React.FC<StartConversationProps> = ({ onSubmit }) => {
  const handleOnSubmit = (e: React.SubmitEvent<HTMLFormElement>) => {
    e.preventDefault();
    onSubmit();
  };
  return (
    <form
      onSubmit={handleOnSubmit}
      className="flex flex-grow justify-center items-center flex-col"
    >
      <button
        type="submit"
        className="w-9/10 p-4 text-gray-900 font-bold text-2xl border-2 border-blue-900 rounded-md hover:bg-blue-500 hover:text-white focus:outline"
      >
        Start conversation
      </button>
    </form>
  );
};

export default StartConversation;
