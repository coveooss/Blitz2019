import * as React from 'react';
import {FastLayer, Rect, Text} from 'react-konva';
import * as _ from 'underscore';
import {blurSize, colors, font, fontSize, fontWeight, smallFontSize, Wall} from './Constants';

export interface IPlayerProps {
    width: number;
    height: number;
    x: number;
    walls: Wall[];
    teams: string[];
    initialWalls: number[];
    reasons: string[];
    step: number;
    speed: number;
}

export class Infos extends React.Component<IPlayerProps> {
    public render() {
        const verticalMargin = 35;
        const smallWidth = Math.min(this.props.width, 400);
        const wallsOffset = this.props.x + smallWidth - 65;
        const getTeamOffset = (i: number) => i * 75 + verticalMargin;
        const teamsInfo = _.map(this.props.teams, (team: string, i: number) => {
            const y = getTeamOffset(i);
            const wallCount = this.props.initialWalls[i] - this.props.walls.filter((w: Wall) => w.team === team).length;
            return [
                <Text
                    key={`team-name-${team}`}
                    x={this.props.x}
                    y={y}
                    width={wallsOffset - this.props.x}
                    fontSize={fontSize}
                    fontFamily={font}
                    fontStyle={fontWeight}
                    fill='#FFFFFF'
                    shadowColor='#FFFFFF'
                    text={team}
                    align='left'
                    wrap='none'
                    ellipsis
                />,
                <Text
                    key={`team-walls-${team}`}
                    x={wallsOffset}
                    y={y}
                    fontSize={fontSize}
                    fontFamily={font}
                    fontStyle={fontWeight}
                    fill='#FFFFFF'
                    shadowColor='#FFFFFF'
                    text={wallCount.toString()}
                    align='left'
                />,
                <Rect
                    key={`team-color-${team}`}
                    x={this.props.x}
                    width={smallWidth}
                    y={y + verticalMargin}
                    height={4}
                    fill={colors[i]}
                    shadowBlur={blurSize}
                    shadowColor={colors[i]}
                />
            ];
        });
        let offsetLogs = 0;
        const getDisconnectOffset = (i: number) => getTeamOffset(this.props.teams.length) + i * 25 + 20;
        const disconnectInfo = this.props.reasons.map((reason: string) => {
            if (!reason) {
                return null;
            }

            const y = getDisconnectOffset(offsetLogs);
            offsetLogs++;

            return [
                <Text
                    key={`team-disconnect-${this.props.teams}`}
                    x={this.props.x}
                    y={y}
                    width={this.props.width}
                    fontSize={smallFontSize}
                    fontFamily={font}
                    fontStyle={fontWeight}
                    fill='#FFFFFF'
                    shadowColor='#FFFFFF'
                    text={reason}
                    align='left'
                    wrap='none'
                />
            ];
        });

        const gameStatusOffset = getDisconnectOffset(offsetLogs) + (offsetLogs > 0 ? verticalMargin : 0);

        return (
            <FastLayer key='infos'>
                <Text
                    key='Step'
                    x={this.props.x}
                    y={gameStatusOffset}
                    fontSize={fontSize}
                    fontFamily={font}
                    fontStyle={fontWeight}
                    fill='#FFF'
                    shadowColor='#FFF'
                    text={`Step: ${Math.max(0, this.props.step + 1)}`}
                    align='left'
                />
                <Text
                    key='Speed'
                    x={this.props.x}
                    y={gameStatusOffset + verticalMargin}
                    fontSize={fontSize}
                    fontFamily={font}
                    fontStyle={fontWeight}
                    fill='#FFF'
                    shadowColor='#FFF'
                    text={`Speed: ${this.props.speed + 1}`}
                    align='right'
                />
                <Text
                    key='start'
                    x={this.props.x}
                    fontSize={fontSize}
                    fontFamily={font}
                    fontStyle={fontWeight}
                    fill='#6EE4CE'
                    shadowColor='#6EE4CE'
                    text='Team'
                    align='left'
                />
                <Text
                    key='end'
                    x={wallsOffset}
                    fontSize={fontSize}
                    fontFamily={font}
                    fontStyle={fontWeight}
                    fill='#6EE4CE'
                    shadowColor='#6EE4CE'
                    text='Walls'
                    align='right'
                />
                {teamsInfo}
                {disconnectInfo}
            </FastLayer>
        );
    }
}
