import PlayerBoard from './PlayerBoard';
import '../index.css';
import BoardLeft from './BoardLeft';
import BoardRight from './BoardRight';
import BoardTop from './BoardTop';

export default function GameBoard() {

    return (
        <div className='gameBoard'>
            <PlayerBoard />
            <br />
            <BoardLeft/>
            <br />
            <BoardRight/>
            <br />
            <BoardTop/>
            <br />
            <MiddleSection />
        </div>
    );
}