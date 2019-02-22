import * as React from 'react';
import {FastLayer, Layer, Rect, Stage, Text} from 'react-konva';
import * as _ from 'underscore';
import { Board } from './Board';
import {blurSize, buttonColors, colors, font, fontSize, fontWeight, keyCodes, speeds, Wall} from './Constants';
import {Icons, renderIcons} from './Icons';
import { Infos } from './Infos';
import {IBlitzVisualization, IDeconnexionReason, IPawnInitialPosition, IPlayerMove} from './IVisualization';
import { Player } from './Player';
import { Walls } from './Walls';

export interface IVisualizationProps {
    game: IBlitzVisualization;
    width: number;
    height: number;
    onEnd: () => void;
    isTV?: boolean;
}

export interface IInitialState {
    teams: string[];
    positions: number[][];
    horizontalWalls: Wall[];
    verticalWalls: Wall[];
    reasons: string[];
    deadTeams: string[];
}

export interface IVisualizationState extends IInitialState {
    isPaused: boolean;
    speed: number;
    step: number;
    winner: number | null;
    hover: string | null;
}

export class Visualization extends React.Component<IVisualizationProps, IVisualizationState> {
    private timer: number | NodeJS.Timer;
    private ref: HTMLInputElement;

    constructor(props: IVisualizationProps, state: IVisualizationState) {
        super(props, state);

        // Add the invalid actions in the replay
        this.props.game.reasons.forEach((reason: IDeconnexionReason|string, i: number) => {
            if (typeof reason !== 'string') {
                const [step, message] = reason['py/tuple'];
                if (message) {
                    const move: IPlayerMove = {'py/tuple': [i, ['invalid', 0, 0]]};
                    this.props.game.actions.splice(step - 1, 0, move);
                }
            }
        });

        this.state = {
            hover: null,
            isPaused: false,
            speed: 0,
            step: -1,
            winner: null,
            ...this.getInitialState(),
        };
    }

    public componentDidMount() {
        this.timer = setTimeout(this.onTimer, 3000);
    }

    public componentWillMount() {
        clearTimeout(this.timer as number);
    }

    public render() {
        const width: number = this.props.width;
        const height: number = this.props.height;

        const numberOfTile: number = this.props.game.initial_board.size;
        const boardSize = Math.min(width, height) * 0.8;

        const tileSize = boardSize / numberOfTile;
        const size = tileSize * 0.65;
        const gap = tileSize * 0.35;

        const infoSize = width - boardSize - size;

        return (
            <div className="Visualization" onClick={() => this.ref.focus()}>
                <Stage width={width} height={height}>
                    <Board size={size} gap={gap} numberOfTile={numberOfTile} goals={this.props.game.initial_board.goals} />
                    <Walls size={size} gap={gap} horizontal={this.state.horizontalWalls} vertical={this.state.verticalWalls} />
                    {this.renderPlayers(size, gap)}
                    {!this.props.isTV && this.renderMainButtons(boardSize)}
                    {!this.props.isTV && this.renderOtherButtons(boardSize)}
                    {this.renderWinner(boardSize)}
                    <Infos
                        width={infoSize}
                        height={height}
                        x={boardSize + gap}
                        walls={[...this.state.horizontalWalls, ...this.state.verticalWalls]}
                        teams={this.props.game.player_names}
                        initialWalls={this.props.game.initial_board.nb_walls}
                        reasons={this.state.reasons || []}
                        step={this.state.step}
                        speed={this.state.speed}
                    />
                </Stage>
                <input
                    ref={(node: HTMLInputElement) => this.ref = node}
                    onKeyPress={(e: React.KeyboardEvent<HTMLInputElement>) => this.onKeyPress(e)}
                    autoFocus={true}
                    defaultValue=''
                    style={{
                        color: 'transparent',
                        backgroundColor: 'transparent',
                        border: 'none',
                        outline: 'none',
                        opacity: 0,
                        zIndex: -1,
                        top: 0,
                        left: 0,
                        position: 'absolute',
                    }}
                />
            </div>
        );
    }

    private getInitialState(): IInitialState {
        const {pawns, horiz_walls, verti_walls} = this.props.game.initial_board;
        const {reasons, deadTeams} = this.getDisconnectReasons(0, false);
        return {
            positions: pawns.map((pawn: IPawnInitialPosition) => pawn['py/tuple']),
            horizontalWalls: horiz_walls.map(position => ({color: 'white', position, team: ''})),
            verticalWalls: verti_walls.map(position => ({color: 'white', position, team: ''})),
            teams: ['Player 1', 'Player 2'],
            reasons,
            deadTeams,
        };
    }

    private onKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
        const gameStart = -1;
        const gameMax = this.props.game.actions.length - 1;
        switch (e.key) {
            case keyCodes.Space:
                this.onTogglePlay();
                break;
            case keyCodes.Z:
                this.goTo(gameStart);
                break;
            case keyCodes.X:
                this.goTo(gameMax);
                break;
            case keyCodes.Comma:
                this.goTo(Math.max(this.state.step - 1, gameStart));
                break;
            case keyCodes.Period:
                this.goTo(Math.min(this.state.step + 1, gameMax));
                break;
            case keyCodes.One:
                this.setState({speed: 0});
                break;
            case keyCodes.Two:
                this.setState({speed: 1});
                break;
            case keyCodes.Three:
                this.setState({speed: 2});
                break;
            case keyCodes.Four:
                this.setState({speed: 3});
                break;
            case keyCodes.Five:
                this.setState({speed: 4});
                break;
            default:
                break;
        }
    }

    private goTo = (step: number) => {
        clearTimeout(this.timer as number);
        this.updateToStep(step, () => {
            if (!this.state.isPaused) {
                this.timer = setTimeout(this.onTimer, speeds[this.state.speed] * 3);
            }
        });
    }

    private onTogglePlay = () => {
        const newIsPaused = !this.state.isPaused;

        if (newIsPaused) {
            clearTimeout(this.timer as number);
        } else {
            this.timer = setTimeout(this.onTimer, speeds[this.state.speed]);
        }

        this.setState({isPaused: newIsPaused});
    }

    private onDecreaseSpeed = () => {
        this.setState({speed: Math.max(this.state.speed - 1, 0)});
    }

    private onIncreaseSpeed = () => {
        this.setState({speed: Math.min(this.state.speed + 1, speeds.length - 1)});
    }

    private renderPlayers(size: number, gap: number) {
        const players = _.map(this.state.positions, ([y, x]: [number, number], i: number) => {
            const posY = y * size + y * gap;
            const posX = x * size + x * gap;
            const isDead = this.state.deadTeams.indexOf(this.props.game.player_names[i]) !== -1;
            return <Player key={i} size={size} color={colors[i]} x={posX} y={posY} isDead={isDead}/>;
        });
        return (
            <FastLayer>{players}</FastLayer>
        );
    }

    private renderMainButtons(size: number) {
        const iconSize = 32;
        const margin = iconSize * 1.3;
        const offset = size / 2 - 2.5 * margin;

        const {hover} = this.state;

        const gameMax = this.props.game.actions.length - 1;

        const actions = {
            speedDown: this.onDecreaseSpeed,
            back: () => this.goTo(Math.max(this.state.step - 1, -1)),
            forward: () => this.goTo(Math.min(this.state.step + 1, gameMax)),
            play: this.onTogglePlay,
            pause: this.onTogglePlay,
            speedUp: this.onIncreaseSpeed,
        };
        const actionsPossible = {
            speedDown: this.state.speed > 0,
            back: this.state.step >= 0,
            forward: this.state.step < gameMax,
            play: this.state.isPaused,
            pause: !this.state.isPaused,
            speedUp: this.state.speed < speeds.length - 1,
        };
        let indexOffset = 0;
        const icons = _.map(_.keys(Icons), (icon: string) => {
            const enabled = actionsPossible[icon];
            const defaultColor = enabled ? buttonColors[0] : buttonColors[2];
            const color = enabled && hover === icon ? buttonColors[1] : defaultColor;
            const x = offset + margin * indexOffset;
            const y = size;
            const renderedIcon = renderIcons[icon]({x, y, fill: color, shadowBlur: blurSize, shadowColor: color, enabled});
            if (renderedIcon) {
                indexOffset++;
            }
            return (
                <React.Fragment key={icon}>
                    {renderedIcon}
                    <Rect
                        x={x}
                        y={y}
                        width={iconSize}
                        height={iconSize}
                        fill='transparent'
                        onMouseEnter={() => enabled && this.setState({hover: icon})}
                        onMouseLeave={() => this.setState({hover: null})}
                        onClick={() => enabled && actions[icon]()}
                    />
                </React.Fragment>
            )
        });

        return (
            <Layer>{icons}</Layer>
        )
    }

    private renderOtherButtons(size: number) {
        const {hover} = this.state;
        const iconSize = 32;
        const margin = iconSize * 1.3;
        const offset = size / 2 - 2.5 * margin;
        const gameMax = this.props.game.actions.length - 1;
        const commonProps = {
            fontFamily: font,
            fontStyle: fontWeight,
            fontSize,
            shadowBlur: blurSize,
            onMouseLeave: () => this.setState({hover: null}),
        };
        const startColor = hover === 'start' ? buttonColors[1] : buttonColors[0];
        const endColor = hover === 'end' ? buttonColors[1] : buttonColors[0];

        return (
            <Layer x={offset} y={size + margin * 1.3}>
                <Text
                    key='start'
                    fill={startColor}
                    shadowColor={startColor}
                    text='Start'
                    align='left'
                    onMouseEnter={() => this.setState({hover: 'start'})}
                    onClick={() => this.goTo(-1)}
                    {...commonProps}
                />
                <Text
                    key='end'
                    x={margin * 4 - 0.3 * margin}
                    fill={endColor}
                    shadowColor={endColor}
                    text='End'
                    align='right'
                    onMouseEnter={() => this.setState({hover: 'end'})}
                    onClick={() => this.goTo(gameMax)}
                    {...commonProps}
                />
            </Layer>
        )
    }

    private renderWinner(width: number) {
        let winnerText = '';
        let ranking: string[] = [];
        const size = width / 9;
        const {players_ranking, player_names} = this.props.game;
        if (this.state.winner !== null) {
            ranking = players_ranking.map((teamNumber: number, index: number) => `${index + 1}. ${player_names[teamNumber]}`);
            winnerText = `Results:\n${ranking.join('\n')}`;
        }
        return (
            <FastLayer>
                <Text
                    fontSize={size}
                    lineHeight={1.2}
                    fill='#6EE4CE'
                    shadowColor='#000000'
                    shadowBlur={blurSize}
                    text={winnerText}
                    wrap="char"
                    align="center"
                    width={width}
                    height={width}
                    verticalAlign="middle"
                />
            </FastLayer>
        );
    }

    private onTimer = () => {
        const newStep = this.state.step + 1;
        this.updateToStep(newStep, () => {
            if (newStep + 1 < this.props.game.actions.length) {
                this.timer = setTimeout(this.onTimer, speeds[this.state.speed]);
            } else if (this.props.onEnd) {
                this.timer = setTimeout(() => this.props.onEnd(), 5000);
            }
        });
    };

    private updateToStep = (step: number, done: () => void) => {
        const {positions, horizontalWalls, verticalWalls} = this.getInitialState();
        const winner = step + 1 <= this.props.game.actions.length - 1
                       ? null
                       : this.props.game.winner;

        for (let currentStep = 0; currentStep <= step; currentStep++) {
            if (this.props.game.actions[currentStep]) {
                const action = this.props.game.actions[currentStep]['py/tuple'];
                const [player, move] = action;
                const [type, y, x] = move;

                if (type === 'P') {
                    // the player {player} moved to y,x
                    positions[player] = [y, x];
                } else if (type === 'WH') {
                    // the player {player} placed an horizontal wall
                    horizontalWalls.push({position: [y, x], color: colors[player], team: this.props.game.player_names[player]});
                } else if (type === 'WV') {
                    // the player {player} placed a vertical wall
                    verticalWalls.push({position: [y, x], color: colors[player], team: this.props.game.player_names[player]});
                }
            }
        }
        const {reasons, deadTeams} = this.getDisconnectReasons(step, winner !== null);

        this.setState({step, positions, horizontalWalls, verticalWalls, winner, reasons, deadTeams}, done);
    }

    private getDisconnectReasons(step: number, hasWinner: boolean): {reasons: string[], deadTeams: string[]} {
        const deadTeams: string[] = [];
        const reasons = this.props.game.reasons
            .map((reason: IDeconnexionReason|string, i: number): IDeconnexionReason => {
                const team = this.props.game.player_names[i];
                if (typeof reason === 'string') {
                    return {team, ['py/tuple']: [-100, reason]};
                }

                return {...reason, team};
            })
            .sort((a: IDeconnexionReason, b: IDeconnexionReason) => {
                const [whenA] = a['py/tuple'];
                const [whenB] = b['py/tuple'];
                return whenA - whenB;
            })
            .map((reason: IDeconnexionReason) => {
                const [when, message] = reason['py/tuple'];
                const err = `Step ${Math.max(0, when)}. ${reason.team}: ${message}`;

                if (message) {
                    const isDeadYet = hasWinner || (when - 1 <= step);
                    if (isDeadYet) {
                        deadTeams.push(reason.team);
                        return err;
                    }
                }

                return '';
            });

        return {reasons, deadTeams}
    }
}
