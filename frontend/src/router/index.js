import { createRouter, createWebHistory } from 'vue-router'

import HomeView from '@/views/HomeView.vue'
import UnknownView from '@/views/UnknownPageView.vue'
import ActivationView from '@/views/ActivationView.vue'

import PlayView from '@/views/PlayView.vue'
/* ************************************************************************** */
import SoloView from '@/views/play/SoloView.vue'
import LocalView from '@/views/play/LocalView.vue'
import MultiplayerView from '@/views/play/MultiplayerView.vue'
import Multiplayer1v1View from '@/views/play/Multiplayer1v1View.vue'
import TournamentMatchmakingView from '@/views/play/TournamentMatchmakingView.vue'
import TournamentView from '@/views/play/TournamentView.vue'
/* ************************************************************************** */

import MiniGameView from '@/views/MiniGameView.vue'
/* ************************************************************************** */
import Pacman1v1 from '@/views/minigame/Pacman1v1.vue'
import PacmanSolo from '@/views/minigame/PacmanSolo.vue'
import GameHistory from '@/views/minigame/GameHistory.vue'
/* ************************************************************************** */
import SettingsView from '@/views/SettingsView.vue'
/* ************************************************************************** */
import SettingsAudioView from '@/views/settings/SettingsAudioView.vue'
import SettingsColorView from '@/views/settings/SettingsColorView.vue'
import SettingsGraphicsView from '@/views/settings/SettingsGraphicsView.vue'
import CreditsView from '@/views/settings/CreditsView.vue'
/* ************************************************************************** */

import LeaderboardView from '@/views/LeaderboardView.vue'
import MyProfileView from '@/views/MyProfileView.vue'
import ProfileView from '@/views/ProfileView.vue'
import SearchProfileView from '@/views/SearchProfileView.vue'
import FriendsView from '@/views/FriendsView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import MatchWon from '@/views/play/MatchWon.vue'

const router = createRouter({
	history: createWebHistory(),
	routes: [
		{
			path: '/',
			name: 'HomeView',
			component: HomeView,
			meta: {
				title: 'ft_transcendence'
			}
		},
		{
			path: '/activation/:uuid',
			name: 'ActivationView',
			component: ActivationView,
			meta: {
				title: 'activation'
			}
		},
		{
			path: '/play',
			name: 'PlayView',
			component: PlayView,
			meta: {
				title: 'play',
			}
		},
		{
			path: '/login',
			name: 'LoginView',
			component: LoginView,
			meta: {
				title: 'login',
			}
		},
		{
			path: '/register',
			name: 'RegisterView',
			component: RegisterView,
			meta: {
				title: 'register',
			}
		},
		{
			path: '/play/solo',
			name: 'SoloView',
			component: SoloView,
			meta: {
				title: 'solo - play',
			}
		},
		{
			path: '/play/local',
			name: 'LocalView',
			component: LocalView,
			meta: {
				title: 'local - play',
			}
		},
		{
			path: '/play/multiplayer',
			name: 'MultiplayerView',
			component: MultiplayerView,
			meta: {
				title: 'multiplayer - play',
			}
		},
		{
			path: '/play/multiplayer/:uuid',
			name: 'Multiplayer1v1View',
			component: Multiplayer1v1View,
			meta: {
				title: '1v1',
			}
		},
		{
			path: '/play/tournament',
			name: 'TournamentMatchmakingView',
			component: TournamentMatchmakingView,
			meta: {
				title: 'tournament matchmaking',
			}
		},
		{
			path: '/play/tournament/:uuid',
			name: 'TournamentView',
			component: TournamentView,
			meta: {
				title: 'tournament',
			}
		},
		{
			path: '/minigame',
			name: 'MiniGameView',
			component: MiniGameView,
			meta: {
				title: 'pacman - mini game',
			}
		},
		{
			path: '/minigame/solo',
			name: 'PacmanSolo',
			component: PacmanSolo,
			meta: {
				title: 'pacman - solo',
			}
		},
		{
			path: '/minigame/1v1',
			name: 'Pacman1v1',
			component: Pacman1v1,
			meta: {
				title: 'pacman - 1v1',
			}
		},
		{
			path: '/minigame/game_history',
			name: 'GameHistory',
			component: GameHistory,
			meta: {
				title: 'pacman - game history',
			}
		},
		{
			path: '/leaderboard',
			name: 'LeaderboardView',
			component: LeaderboardView,
			meta: {
				title: 'leaderboard'
			}
		},
		{
			path: '/profile',
			name: 'MyProfileView',
			component: MyProfileView,
			meta: {
				title: 'my profile'
			}
		},
		{
			path: '/friends',
			name: 'FriendsView',
			component: FriendsView,
			meta: {
				title: 'my friends'
			}
		},
		{
			path: '/searchprofile',
			name: 'SearchProfileView',
			component: SearchProfileView,
			meta: {
				title: 'search profile'
			}
		},
		{
			path: '/profile/:id',
			name: 'ProfileView',
			component: ProfileView,
			meta: {
				title: 'profile'
			}
		},
		{
			path: '/settings',
			name: 'SettingsView',
			component: SettingsView,
			meta: {
				title: 'settings'
			}
		},
		{
			path: '/settings/settings_color',
			name: 'SettingsColorView',
			component: SettingsColorView,
			meta: {
				title: 'color - settings'
			}
		},
		{
			path: '/settings/settings_audio',
			name: 'SettingsAudioView',
			component: SettingsAudioView,
			meta: {
				title: 'audio - settings'
			}
		},
		{
			path: '/settings/settings_graphics',
			name: 'SettingsGraphicsView',
			component: SettingsGraphicsView,
			meta: {
				title: 'graphics - settings'
			}
		},
		{
			path: '/settings/credits',
			name: 'CreditsView',
			component: CreditsView,
			meta: {
				title: 'credit$'
			}
		},
		{
			// juste pour les tests ca va changer -> component et non View
			path: '/play/match_won',
			name: 'MatchWon',
			component: MatchWon,
			meta: {
				title: 'match won'
			}
		},
		{
			path: '/:pathMatch(.*)',
			name: 'UnknownView',
			component: UnknownView,
			meta: {
				title: 'unknown page'
			}
		},
	]
});

router.beforeEach(
	(to, from) => {
		document.title = to.meta?.title ?? 'placeholder title';
	}
);

export default router